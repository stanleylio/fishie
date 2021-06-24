"""stats
SL2021
"""
import sys, time, MySQLdb, statistics
sys.path.append('/home/nuc')
from datetime import datetime, timedelta
from node.helper import dt2ts, ts2dt
import numpy as np


def active():
    conn = MySQLdb.connect('localhost', user='webapp', charset='utf8mb4')
    cur = conn.cursor()

    now = time.time()

    cur.execute(f"""select nodeid from uhcm.devices where nodeid like 'node-%' order by nodeid""")
    nodes = [x[0] for x in list(cur.fetchall())]
    messagecount = [0 for node in nodes]
    for k,node in enumerate(nodes):
        cur.execute(f"""select COUNT(*)
                        from uhcm.`{node}`
                        WHERE ReceptionTime between %s and %s""", (now - 24*60*60, now, ))
        r = cur.fetchone()[0]
        #print(node, r)
        messagecount[k] = r

    nodecount = sum([1 if x > 0 else 0 for x in messagecount])

    d = {'ts':time.time(),
         'activenodecount':nodecount,
         'min':min(messagecount),
         'max':max(messagecount),
         'sum':sum(messagecount),
         'median (non-zero)':statistics.median(filter(lambda x: x > 0, messagecount)),
         'mean':statistics.mean(filter(lambda x: x > 0, messagecount)),
         }
    return d


def hourly():
    # past Nd days, up to the beginning of this hour
    end = datetime.utcnow().replace(minute=0).replace(second=0).replace(microsecond=0)
    x = [end - timedelta(hours=i) for i in range(Nd*24, 0, -1)]

    conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
    cur = conn.cursor()


    cur.execute(f"""select nodeid from uhcm.devices order by nodeid""")
    nodes = [x[0] for x in list(cur.fetchall())]

    D = {}
    for node in nodes:
        c = [0 for _ in x]
        for k, xx in enumerate(x):
            cmd = f"""select count(*) from uhcm.`{node}`
                        where ReceptionTime between %s and %s"""
            cur.execute(cmd, (dt2ts(xx), dt2ts(xx + timedelta(hours=1)), ))
            c[k] = cur.fetchone()[0]
        D[node] = c
        #print(node, json.dumps(d[node], separators=(',',':')))

    ts = [int(dt2ts(xx)) for xx in x]

    # diff(2)
    ts = np.diff(ts, n=2, prepend=[0, 0]).tolist()
    for node in nodes:
        D[node] = np.diff(D[node], n=2, prepend=[0, 0]).tolist()

    D = {'ts':ts,
         'count':D,
         }
    return D



if '__main__' == __name__:

    import json

    Nd = 31

    D = active()
    H = hourly()
    
    print(f"""{D['activenodecount']} nodes transmitted {D['sum']:,} messages in the past 24 hours.""")
    print('24 hr message count')
    print(f"min: {D['min']}")
    print(f"max: {D['max']:,}")
    print(f"sum: {D['sum']:,}")
    print(f"median (non-zero): {D['median (non-zero)']}")
    print(f"mean: {D['mean']:.1f}")

    with open('/var/www/uhcm/active.json', 'w', 1) as f:
        f.write(json.dumps(D, separators=(',',':')))
    with open('/var/www/uhcm/hourly.json', 'w', 1) as f:
        f.write(json.dumps(H, separators=(',',':')))

