import sqlite3, json, sys
from os import getcwd
from os.path import realpath, join, dirname

encode = lambda x: json.dumps(x, separators=(',', ':'), ensure_ascii=False)
decode = lambda s: json.loads(s)
__location__ = realpath(join(getcwd(), dirname(__file__)))
path_to_config = join(__location__, 'config.db')

'''print('- - - - -')
c.execute("SELECT * FROM config WHERE nodeid=?", (json.dumps('node-189'),))
for row in c.fetchall():
    print(row)

print('- - - - -')
c.execute("SELECT * FROM config WHERE site=?", (json.dumps('sc'),))
for row in c.fetchall():
    print(row)

print('- - - - -')
c.execute("SELECT * FROM config WHERE nodeid LIKE ?", (json.dumps('base-%'),))
for row in c.fetchall():
    print(row)

print('- - - - -')
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE \"base-%\"")
for row in c.fetchall():
    print(row[0])

print('- - - - -')
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in c.fetchall():
    print(row[0])'''

def _config_import():
    src = sqlite3.connect(path_to_config)
    dst = sqlite3.connect(':memory:')
    c = dst.cursor()
    for line in src.iterdump():
        #c.execute(line)    # doesn't work for some reason. backup() is also not available until Python 3.7.
        c.executescript(line)
    return dst
    
def config_as_dict():
    config = {}
    conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT site,nodeid FROM config ORDER BY nodeid")
    for row in c.fetchall():
        k,v = decode(row[0]), decode(row[1])
        if k not in config:
            config[k] = []
        config[k].append(v)
    conn.commit()
    conn.close()
    return config

def get_site(nodeid):
    conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT site FROM config WHERE nodeid=?", (encode(nodeid),))
    row = c.fetchone()
    site = decode(row[0]) if row is not None else None
    conn.commit()
    conn.close()
    return site

def get_list_of_sites(conn=None):
    if conn is None:
        conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT DISTINCT site FROM config")
    L = [decode(row[0]) for row in c.fetchall()]
    conn.commit()
    if conn is None:
        conn.close()
    return L

def get_list_of_devices(*, site=None, conn=None):
    if conn is None:
        conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    if site is None:
        c.execute("SELECT nodeid FROM config ORDER BY nodeid")
    else:
        c.execute("SELECT nodeid FROM config WHERE site=? ORDER BY nodeid", (encode(site),))
    L = [decode(row[0]) for row in c.fetchall()]
    conn.commit()
    if conn is None:
        conn.close()
    return L

'''def get_list_of_nodes(*, site=None):
    config = {}
    conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    if site is None:
        c.execute("SELECT nodeid FROM config WHERE nodeid LIKE ? ORDER BY nodeid", (encode('node-%'), ))
    else:
        c.execute("SELECT nodeid FROM config WHERE site=? AND nodeid LIKE ? ORDER BY nodeid", (encode(site), encode('node-%'), ))
    L = [decode(row[0]) for row in c.fetchall()]
    conn.commit()
    conn.close()
    return L'''

def get_list_of_variables(nodeid, conn=None):
    if conn is None:
        conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT variable_name FROM '{}'".format(nodeid + '_variables'))   # "magic"... hidden conventions...
    L = [decode(row[0]) for row in c.fetchall()]
    conn.commit()
    if conn is None:
        conn.close()
    return L

def get_node_attribute(nodeid, attribute, conn=None):
    if conn is None:
        conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT {} from 'config' WHERE nodeid=?".format(attribute, nodeid), (encode(nodeid),))
    row = c.fetchone()
    v = decode(row[0]) if row is not None else None
    conn.commit()
    if conn is None:
        conn.close()
    return v

def get_variable_attribute(nodeid, variable, attribute, conn=None):
    if conn is None:
        conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT {} from '{}_variables' WHERE variable_name=?".format(attribute, nodeid), (encode(variable),))
    row = c.fetchone()
    v = decode(row[0]) if row is not None else None
    conn.commit()
    if conn is None:
        conn.close()
    return v

def get_list_of_disp_vars(nodeid, conn=None):
    if conn is None:
        conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT variable_name FROM '{}' WHERE plot=?".format(nodeid + '_variables'), (encode(True),))   # "magic"... hidden conventions...
    L = [decode(row[0]) for row in c.fetchall()]
    conn.commit()
    if conn is None:
        conn.close()
    return L

'''def get_range(nodeid, variable):
    conn = sqlite3.connect(path_to_config)
    c = conn.cursor()
    c.execute("SELECT lower_bound,upper_bound FROM '{}' WHERE variable_name=?".format(nodeid + '_variables'), (encode(variable),))   # "magic"... hidden conventions...
    row = c.fetchone()
    conn.commit()
    conn.close()
    return decode(row[0]),decode(row[1])'''

'''def is_in_range(nodeid, variable, reading):
    r = get_range(nodeid, variable)
    return reading >= min(r) and reading <= max(r)'''
    

if '__main__' == __name__:
    print(config_as_dict())
    print(get_site('node-224'))
    print(get_list_of_sites())
    print(get_list_of_devices(site='poh'))
    #print(get_list_of_nodes(site='poh'))
    print(get_list_of_variables('node-189'))
    print(get_variable_attribute('node-183', 'O2', 'unit'))
    print(get_variable_attribute('node-183', 'O2', 'description'))
    print(get_variable_attribute('node-183', 'O2', 'interval_second'))
    print(get_variable_attribute('node-183', 'O2', 'plot_range_second'))
    print(get_list_of_disp_vars('node-189'))
    #print(get_range('node-189', 'O2'))
    #print(is_in_range('node-189', 'O2', 123))
