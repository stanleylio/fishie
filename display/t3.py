# calculate and plot the # of samples received per hour
# in the past N days for all nodes
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import sys, MySQLdb
sys.path.append('/home/nuc')
from os.path import expanduser
from datetime import datetime, timedelta
from node.helper import dt2ts, ts2dt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

Nd = 30

plotfilename = '/var/www/uhcm/img/sample_count.png'

conn = MySQLdb.connect(host='localhost', user='webapp', charset='utf8mb4')
cur = conn.cursor()

end = datetime.utcnow().replace(minute=0).replace(second=0).replace(microsecond=0)
begin = end - timedelta(hours=Nd*24)
begin = dt2ts(begin)
end = dt2ts(end)

# - - -
print('counting...')
R = {}
cur.execute("""SELECT nodeid FROM uhcm.devices ORDER BY nodeid""")
tables, = list(zip(*cur.fetchall()))
for table in tables:
    cur.execute("""SELECT name FROM uhcm.variables WHERE nodeid=%s""", (table, ))
    tmp = list(zip(*cur.fetchall()))
    if 0 == len(tmp):
        # no variable
        continue
    columns, = tmp
    time_col = 'ReceptionTime'

    # this is fast, but you miss all the nodes that did not report
    # anything in the plot.
    cmd = """SELECT MAX({time_col}) AS idx,
                    DATE_FORMAT(FROM_UNIXTIME({time_col}), '%%Y%%m%%d%%H') AS tss,
                    COUNT({time_col})
            FROM uhcm.`{table}`
            WHERE {time_col} between %s AND %s
            GROUP BY tss
            ORDER BY idx ASC""".format(table=table, time_col=time_col)
    cur.execute(cmd, (begin, end, ))
    tmp = list(zip(*cur.fetchall()))
    if 0 == len(tmp):
        # no data
        R[table] = [[begin, end], [0, 0]]
        continue
    x,_,y = tmp
    R[table] = [x, y]

# - - -
print('plotting...')

fig, axes = plt.subplots(len(R), 1, figsize=(8, 200), sharex=True, dpi=75)

for i, table in enumerate(sorted(R.keys())):
    x = [ts2dt(tmp) - timedelta(hours=10) for tmp in R[table][0]]
    y = R[table][1]
    
    axes[i].plot(x, y, marker=None, linestyle='-', color='#1f77b4')
    #axes.fill_between(x, 0, y, color='#9ed7ff')
    axes[i].fill_between(x, 0, y, color='#1f77b4', alpha=0.3)
    # why is vertical alignment always so difficult?
    #axes[i].text(ts2dt((begin + end)/2),
    #             (axes[i].get_ylim()[0] + axes[i].get_ylim()[1])/2,
    #             table,
    #             fontsize=10,
    #             alpha=0.4,
    #             va='center', ha='center')
    axes[i].locator_params(nbins=2, axis='y')     # max 2 labels on y axis
    axes[i].set_ylim(0, axes[i].get_ylim()[1])    # y axis lower limit = 0
    #axes[i].set_title(table)
    axes[i].set_ylabel(table, rotation='horizontal', ha='right', va='center')
    axes[i].grid(False)

axes[-1].set_xlabel('HST')

fig.tight_layout()
fig.autofmt_xdate()
plt.savefig(plotfilename, dpi=300, bbox_inches='tight')
