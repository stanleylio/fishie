# calculate and plot the # of samples received per hour
# in the past N days for all nodes
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import sys,time,itertools,MySQLdb
sys.path.append('/home/nuc')
from os.path import expanduser
from datetime import datetime,timedelta
from node.storage.storage2 import storage,auto_time_col
from node.helper import dt2ts,ts2dt
from cred import cred
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


Nd = 30


plotfilename = '/var/www/uhcm/img/sample_count.png'
host = 'localhost'
user = 'root'
password = cred['mysql']
dbname = 'uhcm'
conn = MySQLdb.connect(host=host,user=user,passwd=password,db=dbname)
cur = conn.cursor()

store = storage()

now = datetime.utcnow()
now = now.replace(minute=0).replace(second=0).replace(microsecond=0)

i = range(Nd*24,0,-1)
begins = [now - timedelta(hours=tmp) for tmp in i]
ends = [tmp + timedelta(hours=1) for tmp in begins]
begins = [dt2ts(tmp) for tmp in begins]
ends = [dt2ts(tmp) for tmp in ends]

R = {}
for table in store.get_list_of_tables():
    #if len(R) >= 10:
    #    break
    print(table)
    time_col = auto_time_col(store.get_list_of_columns(table))
    d = []
    for begin,end in zip(begins,ends):
        cmd = 'SELECT COUNT(*) FROM {dbname}.`{table}` WHERE {time_col} >= {begin} AND {time_col} <= {end}'.\
              format(dbname=dbname,table=table,time_col=time_col,begin=begin,end=end)
        #print cmd
        cur.execute(cmd)
        r = cur.fetchall()
        d.append((end,list(r)[0][0]))
    R[table] = zip(*d)


# - - - - -
fig,ax = plt.subplots(len(R),1,sharex=True,figsize=(8,120),dpi=80)
i = 1
for table,r in sorted(R.iteritems()):
    ax = plt.subplot(len(R),1,i)
    i += 1

    x = [ts2dt(tmp) - timedelta(hours=10) for tmp in r[0]]
    y = r[1]
    ax.plot_date(x, y, marker=None, linestyle='-', color='#1f77b4')
    #ax.fill_between(x,0,y,color='#9ed7ff')
    ax.fill_between(x, 0, y, color='#1f77b4', alpha=0.3)
    # why is vertical alignment always so difficult?
    #ax.text(ts2dt((min(r[0]) + max(r[0]))/2.0), 0, table, fontsize=30, alpha=0.2, verticalalignment='bottom', horizontalalignment='center')
    ax.locator_params(nbins=3, axis='y')     # max 3+1 labels on y axis
    ax.set_ylim(0, plt.ylim()[1])            # y axis lower limit = 0
    ax.set_title(table)
    ax.grid(False)

fig.tight_layout()
fig.autofmt_xdate()
plt.savefig(plotfilename,dpi=300,bbox_inches='tight')
