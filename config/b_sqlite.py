# Convert the info in the .py config files into an sqlite database.
# Supposed to be an one-off script. Future changes to config should be done directly in the sqlite database. The .py files should be removed.
# Values are encoded in json (see the function encode()).
#
# All columns are of type TEXT, and values are encoded as JSON. Annoying when writing queries, but that makes storing NaN and +/-Inf possible.
#
# Note 1: ReceptionTime is not listed in the .py files. It is added here as ReceptionTime DOUBLE NOT NULL. The PRIMARY KEY() part can only be added at MySQL table creation.
# Note 2: Some columns have been dropped; some have been renamed; default values have been made explicit.
# Note 3: Some units have been standardized (e.g. Deg.C, \u00b0C -> \u2103).
#
# SL20200410
import sys, re, json, sqlite3
from pathlib import Path
from os.path import join, split
from importlib import import_module
from datetime import timedelta


# Return a list of directory or files in p.
# Directory-only if d; file-only if not d.
def f(p, d):
    return [ff for ff in Path(p).iterdir() if ff.is_dir() == d]

# nothing beats hard-coded magic consts...
attributes = ['nodeid', 'name', 'site', 'note', 'status', 'longitude', 'latitude', 'location', 'tags', 'coreid', ]
variables = ['variable_name', 'description', 'unit', 'lower_bound', 'upper_bound', 'interval_second', 'plot', 'plot_range_second', 'db_type', ]

encode = lambda x: json.dumps(x, separators=(',', ':'), ensure_ascii=False)

# I don't know. I like sqlite better than a bunch of CSVs. Or put the config in MySQL instead of having another db.

conn = sqlite3.connect('config.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS 'config';")
cols = ["{} TEXT".format(c) for c in attributes]
cmd = "CREATE TABLE 'config' ({cols},UNIQUE(nodeid));".format(cols=','.join(cols))
c.execute(cmd)
conn.commit()


for folder in f(r'.', True):
    tmp = [tmp for tmp in f(folder, False) if re.match('^((base)|(node))_\d+\.py$', split(str(tmp))[-1])]
    for device in tmp:
        print(device)
        
        name = folder.name + '.' + str(device.name)[:-3]
        x = import_module(name)
        d = {attr: encode(getattr(x, attr, '')) for attr in attributes}

        # new cols: nodeid, site, db_type
        site, nodeid = x.__name__.split('.')
        nodeid = nodeid.replace('_', '-')
        d.update({'nodeid': encode(nodeid), 'site': encode(site), })
        #print(d['nodeid'])

        # patch
        if d.get('note', None) in ['(TBD)', '-']:
            d['note'] = encode('')

        cmd = "INSERT INTO 'config' VALUES ({})".format(','.join(['?']*len(attributes)))
        #print(cmd)
        c.execute(cmd, [d[k] for k in attributes])

        # - - -
        # variables of a device (the "conf" list of dicts)
        if hasattr(x, 'conf'):
            c.execute("DROP TABLE IF EXISTS '{}_variables';".format(nodeid))
            cols = ["{} TEXT".format(c) for c in variables]
            cmd = "CREATE TABLE '{}_variables' ({},UNIQUE(variable_name));".format(nodeid, ','.join(cols))
            c.execute(cmd)
            conn.commit()

            cmd = "INSERT INTO '{}_variables' VALUES ({})".format(nodeid, ','.join(['?']*len(variables)))
            
            # HACK - patch in ReceptionTime (not stated in the .py config files; added by storage2.py)
            rt = {'variable_name':encode('ReceptionTime'),
                  'description':encode(''),
                  'unit':encode(''),
                  'lower_bound':encode(float('-inf')),
                  'upper_bound':encode(float('inf')),
                  'interval_second':encode(float('nan')),
                  'plot':encode(False),
                  'plot_range_second':encode(0),
                  'db_type':'DOUBLE NOT NULL'}
          
            c.execute(cmd, [rt[k] for k in variables])
            
            for field in x.conf:
                # HACK - there are two parts to this. It needs to be NOT NULL, but the PRIMARY KEY() part can only be done at table creation (the actual data table, not this schema table here.)
                _type = encode('DOUBLE')
                if field['dbtag'] in ['ReceptionTime']:
                    _type = encode('DOUBLE NOT NULL')

                d = dict(zip(variables,
                             (encode(field['dbtag']),
                              encode(field['description']),
                              encode(field.get('unit', '')),
                              encode(field.get('lb', float('-inf'))),
                              encode(field.get('ub', float('inf'))),
                              encode(field.get('interval', float('nan'))),
                              encode(field.get('plot', True)),
                              encode(field.get('plot_range', int(timedelta(days=7).total_seconds()))),
                              _type,
                              )))

                # HACK - unit standardization
                if d.get('unit', None) in ['Deg.C', '\u00b0C']:
                    d['unit'] = '\u2103'
                if d.get('unit', None) == 'uM':
                    d['unit'] = '\u03bcM'

                c.execute(cmd, [d[k] for k in variables])
                
conn.commit()
conn.close()
