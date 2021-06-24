import json, sys, MySQLdb
from os import getcwd
from os.path import realpath, join, dirname

def config_as_dict():
    conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
    c = conn.cursor()
    c.execute("SELECT site,nodeid FROM uhcm.`devices` ORDER BY `nodeid`")
    config = {}
    for k,v in c.fetchall():
        if k not in config:
            config[k] = []
        config[k].append(v)
    conn.close()
    return config

def config_as_list():
    conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
    c = conn.cursor()
    c.execute("SELECT nodeid,site,name,location,deployment_status FROM uhcm.`devices` ORDER BY `site`")
    config = list(c.fetchall())
    conn.close()
    return config

def get_site(nodeid):
    conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
    c = conn.cursor()
    c.execute("SELECT site FROM uhcm.`devices` WHERE nodeid=%s", (nodeid,))
    row = c.fetchone()
    site = row[0] if row is not None else None
    conn.close()
    return site

def get_list_of_sites(*, conn=None):
    should_close = False
    if conn is None:
        conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
        should_close = True
    c = conn.cursor()
    c.execute("SELECT DISTINCT site FROM uhcm.`devices`")
    L = [row[0] for row in c.fetchall()]
    if should_close:
        conn.close()
    return L

def get_list_of_devices(*, site=None, conn=None):
    should_close = conn is None
    if conn is None:
        conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
    c = conn.cursor()
    if site is None:
        c.execute("SELECT nodeid FROM uhcm.`devices` ORDER BY `nodeid`")
    else:
        c.execute("SELECT nodeid FROM uhcm.`devices` WHERE site=%s ORDER BY `nodeid`", (site,))
    L = [row[0] for row in c.fetchall()]
    if should_close:
        conn.close()
    return L

def get_list_of_variables(nodeid):
    conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
    c = conn.cursor()
    c.execute("SELECT name FROM uhcm.`variables` WHERE nodeid=%s", (nodeid,))
    L = [row[0] for row in c.fetchall()]
    conn.close()
    return L

def get_node_attribute(nodeid, attribute, *, conn=None):
    should_close = False
    if conn is None:
        conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
        should_close = True
    c = conn.cursor()
    c.execute("SELECT `{}` from uhcm.`devices` WHERE nodeid=%s".format(attribute), (nodeid,))
    row = c.fetchone()
    if should_close:
        conn.close()
    return row[0] if row else None

def get_variable_attribute(nodeid, variable, attribute, *, conn=None):
    should_close = False
    if conn is None:
        conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
        should_close = True
    c = conn.cursor()
    c.execute("SELECT `{}` from uhcm.`variables` WHERE nodeid=%s AND name=%s".format(attribute), (nodeid, variable,))
    row = c.fetchone()
    L = row[0] if row is not None else None
    if should_close:
        conn.close()
    return L

def get_list_of_disp_vars(nodeid, *, conn=None):
    should_close = False
    if conn is None:
        conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
        should_close = True
    c = conn.cursor()
    c.execute("SELECT `name` FROM uhcm.`variables` WHERE nodeid=%s AND plot=%s", (nodeid, True,))
    L = [row[0] for row in c.fetchall()]
    if should_close:
        conn.close()
    return L

def coreid2nodeid(coreid):
    conn = MySQLdb.connect(host='localhost', user='webapp', passwd='', db='uhcm', charset='utf8mb4')
    c = conn.cursor()
    c.execute("SELECT nodeid from uhcm.`devices` WHERE coreid=%s", (coreid,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


if '__main__' == __name__:
    print(config_as_dict())
    print(get_site('node-224'))
    print(get_list_of_sites())
    print(get_list_of_devices(site='poh'))
    print(get_list_of_variables('node-189'))
    print(get_node_attribute('node-206', 'site'))
    print(get_variable_attribute('node-183', 'O2', 'unit'))
    print(get_variable_attribute('node-183', 'O2', 'description'))
    print(get_variable_attribute('node-183', 'O2', 'interval_second'))
    print(get_variable_attribute('node-183', 'O2', 'plot_range_second'))
    print(get_list_of_disp_vars('node-189'))
