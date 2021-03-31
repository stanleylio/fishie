# Note 1: ReceptionTime is not listed in the .py files. It is added here as ReceptionTime DOUBLE NOT NULL. The PRIMARY KEY() part can only be added at MySQL table creation.
# Note 2: Some columns have been dropped; some have been renamed; default values have been made explicit.
# Note 3: Some units have been standardized (e.g. Deg.C, \u00b0C -> \u2103).
import sys, re, json, MySQLdb, math
from pathlib import Path
from os.path import join, split
from importlib import import_module
from datetime import timedelta


# Return a list of directory or files in p.
# Directory-only if d; file-only if not d.
def f(p, d):
    return [ff for ff in Path(p).iterdir() if ff.is_dir() == d]

conn = MySQLdb.connect(host='localhost', user='s', db='uhcm', charset='utf8mb4')
c = conn.cursor()


# nothing beats hard-coded magic consts...
attributes = ['nodeid', 'name', 'site', 'note', 'status', 'longitude', 'latitude', 'altitude_meter', 'location', 'tags', 'coreid', 'time_col', ]
M = {'nodeid': 'VARCHAR(64) UNIQUE NOT NULL',
     'latitude': 'FLOAT',
     'longitude': 'FLOAT',
     'altitude_meter': 'FLOAT',
     'coreid': 'VARCHAR(32) UNIQUE',
     }
def cf(x):
    try:
        return float(x)
    except:
        return None
F = {'latitude': cf,
     'longitude': cf,
     'altitude_meter': cf,
     }

c.execute("DROP TABLE IF EXISTS uhcm.`devices`;")
cmd = 'CREATE TABLE uhcm.`devices` ('
tmp = ['`{}` {}'.format(col, M.get(col, 'TEXT')) for col in attributes]
cmd += ','.join(tmp)
cmd += ', PRIMARY KEY(`nodeid`)) CHARACTER SET utf8mb4;'
c.execute(cmd)
conn.commit()

PYCONFIGS = {}

for folder in f(r'.', True):
    tmp = [tmp for tmp in f(folder, False) if re.match('^((base)|(node))_\d+\.py$', split(str(tmp))[-1])]
    for device in tmp:
        #print(device)
        
        name = folder.name + '.' + str(device.name)[:-3]
        x = import_module(name)
        d = {attr: getattr(x, attr, '') for attr in attributes}

        # patches
        # new cols: nodeid, site, db_type
        site, nodeid = x.__name__.split('.')
        nodeid = nodeid.replace('_', '-')
        # hack - for later use
        PYCONFIGS[nodeid] = x
        
        d.update({'nodeid': nodeid, 'site': site, })
        if d.get('note', None) in ['(TBD)', '-']:
            d['note'] = ''
        if d.get('coreid', '') in ['']:
            d['coreid'] = None
        if type(d.get('tags', '')) in [list]:
            d['tags'] = ','.join(d['tags'])
        if d.get('location', None) in ['(TBD)', '-', '']:
            d['location'] = ''
        # If time_col is explicitly defined, use that. If not, then look
        # into the variables to see if either 'ts' or 'Timestamp' is
        # defined. If neither is, then default to 'ReceptionTime'.
        #
        # Design note: having a default here means the auto_time_col
        # code in the webapp won't work since it'd never be NULL/'' when
        # undefined. But if you do all the auto stuff here then you
        # won't need an auto_time_col to begin with. Of course then this
        # becomes yet another precond you need to test. Also without a
        # live ts vs. ReceptionTime sanity check, a broken RTC on the
        # instruments will not be detected.
        # (note: manually define time_col to override default)
        if 0 == len(d.get('time_col', '')):     # Note: getattr() above defaults to '' if None
            for t in ['ts', 'Timestamp']:
                if t in [c['dbtag'] for c in getattr(PYCONFIGS[nodeid], 'conf', [])]:   # (some don't have any variables)
                    d['time_col'] = t
                    break
            else:
                # "neither 'ts' nor 'Timestamp' is defined. Default to 'ReceptionTime'"
                d['time_col'] = 'ReceptionTime'

        cmd = "INSERT INTO uhcm.`devices` VALUES ({})".format(','.join(['%s']*len(attributes)))
        d = [F.get(k, lambda x: x)(d[k]) for k in attributes]
        c.execute(cmd, d)

conn.commit()


# - - - - -


M = {'nodeid': 'VARCHAR(64) NOT NULL',
     'name': 'VARCHAR(32) NOT NULL',
     'lower_bound': 'FLOAT',
     'upper_bound': 'FLOAT',
     'interval_second': 'FLOAT',
     'plot_range_second': 'FLOAT',
     }
def cf(x):
    try:
        #return json.dumps(x, ensure_ascii=False)
        x = float(x)
        if math.isinf(x) or math.isnan(x):
            return None
        return x
    except:
        #raise
        return None
F = {'lower_bound': cf,
     'upper_bound': cf,
     'interval_second': cf,
     'plot_range_second': cf,
     }
# a table of variable definitions
variables = ['nodeid', 'name', 'description', 'unit', 'lower_bound', 'upper_bound', 'interval_second', 'plot', 'plot_range_second', 'db_type', ]
c.execute("DROP TABLE IF EXISTS uhcm.`variables`;")
cmd = 'CREATE TABLE uhcm.`variables` ('
tmp = ['`{}` {}'.format(col, M.get(col, 'TEXT')) for col in variables]
cmd += ','.join(tmp)
cmd += ', PRIMARY KEY(`nodeid`, `name`)) CHARACTER SET utf8mb4;'
c.execute(cmd)
conn.commit()


c.execute("select `nodeid` from uhcm.`devices`")
for nodeid, in c.fetchall():
    #print(nodeid, PYCONFIGS[nodeid])

    if not hasattr(PYCONFIGS[nodeid], 'conf'):
        print('WARNING: no conf for {}'.format(nodeid))
        continue

    cmd = "INSERT INTO uhcm.`variables` VALUES ({})".format(','.join(['%s']*len(variables)))

    # patch in ReceptionTime (not declared in the .py config files; was to be added by storage2.py)
    rt = {'nodeid':nodeid,
          'name':'ReceptionTime',
          'description':'Server time when data reached server; UTC',
          'unit':None,
          'lower_bound':None,
          'upper_bound':None,
          'interval_second':None,
          'plot':0,
          'plot_range_second':0,
          'db_type':'DOUBLE NOT NULL'}
    c.execute(cmd, [rt[k] for k in variables])

    #print(PYCONFIGS[nodeid].conf)
    for field in PYCONFIGS[nodeid].conf:
        #print(nodeid, field)
        
        d = dict(zip(variables,
                     (nodeid,
                      field['dbtag'],
                      field['description'],
                      field.get('unit', ''),
                      field.get('lb', None),
                      field.get('ub', None),
                      field.get('interval', None),
                      field.get('plot', 1),
                      field.get('plot_range', 7*24)*3600,
                      'DOUBLE',
                      )))
        # patches
        if d.get('description', '') in ['-']:
            d['description'] = ''
        if d.get('unit', None) in ['DegC', 'Deg.C', '\u00b0C']:
            d['unit'] = '\u2103'
        if d.get('unit', None) == 'uM':
            d['unit'] = '\u03bcM'

        c.execute(cmd, [d[k] for k in variables])
        

conn.commit()
conn.close()
print('Done.')
