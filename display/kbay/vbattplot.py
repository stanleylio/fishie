# deployment checklist:
# enable CTD
# clear memory
# set operation time window
# measure Vcc
# record serial number
# replace battery

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import traceback,sys
sys.path.append('/home/nuc/node')
from helper import ts2dt


cutoff = 3.5

#fn = 'coco.txt'
#fn = 'monty.txt'
fn = sys.argv[1]


with open(fn) as f:
    lines = f.readlines()

T,V = [],[]
for line in lines:
    try:
        line = line.strip().split('\t')
        ts = float(line[1])
        if ts >= 1473796279.810314:
            line = line[2].split(',')
            if 8 == len(line):
                T.append(ts)
                V.append(float(line[7]))
    except:
        pass


#T = [datetime.strptime(t,'%Y-%m-%dT%H:%M:%S.%f') for t in T]
T = [ts2dt(tmp) for tmp in T]
T = [tmp - min(T) for tmp in T]
T = [tmp.total_seconds()/3600./24. for tmp in T]

V = [float(v) for v in V]


# - - - - -
p = np.polyfit(T,V,1)
p = np.poly1d(p)
i = 0
while p(i) > cutoff:
    i = i + 0.1
bi = i
print 'Current runtime: {}'.format(timedelta(days=max(T)))
print 'Battery life estimate: {} days'.format(bi)

x = np.linspace(0,bi,100)

# - - - - -
fig,ax = plt.subplots()
ax.plot(T,V,'.-',color='b',label='measurements')
ax.plot(x,p(x),':',color='b',label='estimated {} days'.format(bi))

ax.set_xlabel('Time Elapsed (days)')
ax.set_ylabel('Vbatt, V')
ax.set_title('Telemetry Dongle Battery Voltage')
ax.grid(True)

from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')
h,l = ax.get_legend_handles_labels()
ax.legend(h,l,loc='upper right',prop=fontP)

#fig.autofmt_xdate()
fig.savefig(fn + '.png',dpi=600)


plt.show()

