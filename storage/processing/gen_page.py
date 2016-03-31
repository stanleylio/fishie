# -*- coding: utf-8 -*-
from jinja2 import Template
from json import dumps


# - - - - -
#ts = [0,1,2,3]
#x = [2,3,4,5]
#xlabel = 'Date/time'
#ylabel = 'thus spoke zarathustra'
#title = 'four legs good two legs bad'
#linelabel = 'the central tenet'
template = 'template.html'
output = 'index.html'
# - - - - -


# - - - - -
node = 'node_004'
variable = 'Pressure_BMP180'
time_col = 'ReceptionTime'

import calendar
def dt2ts(dt):
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

from storage import storage_read_only
store = storage_read_only()
for table in store.get_list_of_tables():
    print table
    for v in store.get_list_of_columns(table):
        print '\t',v

tmp = store.read_all(node)
print('{} samples'.format(len(tmp[variable])))
ts = [dt2ts(v) for v in tmp[time_col]]
x = tmp[variable]

from helper import median_of_group
ts,x = median_of_group(ts,x)
xlabel = 'Date/Time'
ylabel = 'ylabel'
title = node
linelabel = ''
# - - - - -

ts = dumps(ts,separators=(',',':'))
x = dumps(x,separators=(',',':'))
xlabel = dumps(xlabel)
ylabel = dumps(ylabel)
title = dumps(title)
linelabel = dumps(linelabel)

with open(template,'r') as f,\
     open(output,'w') as fout:
    t = Template(f.read())
    s = t.render(ts=ts,x=x,xlabel=xlabel,ylabel=ylabel,title=title,linelabel=linelabel)
    fout.write(s)




