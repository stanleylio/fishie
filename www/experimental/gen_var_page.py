#!/usr/bin/python
import cgi,cgitb,json,time,sys
sys.path.append('../../')
sys.path.append('../../storage')
from jinja2 import Template
from storage import storage
from config_support import read_disp_config,get_unit,get_color

cgitb.enable(display=1)

time_col = 'Timestamp'

print 'Content-Type: text/html\n'   # don't forget the '\n'

form = cgi.FieldStorage()
node_id = form.getlist('node_id')
if len(node_id) > 0:
    node_id = int(node_id[0])
else:
    node_id = 4
dbtags = form.getlist('var')
nhour = form.getlist('nhour')
if len(nhour) > 0:
    nhour = float(nhour[0])
    avg = None
else:
    nhour = 7*24
    avg = 'hourly'


# for debugging
#node_id = 4
#dbtags = ['Pressure_MS5803','Temp_MS5803','Temp_BMP180']
#linecolors = ['gold','red','blue']
#nhour = 5


store = storage()

tmp = read_disp_config()
if len(dbtags) <= 0:
    dbtags = tmp[node_id]['variable']
units = get_unit(node_id,dbtags)
linecolors = get_color(node_id,dbtags)

data = []
title_strs = []

retrieved = store.read(node_id,variables=dbtags,nhour=nhour,avg=avg)

for k,tag in enumerate(dbtags):
    if retrieved is not None:
        ts = tuple(time.mktime(t.timetuple()) for t in retrieved[time_col])
        dp = retrieved[tag]

        if 'Pressure_BMP180' == tag:
            dp = tuple(v/1000. for v in dp)     # wait what? no tuple comprehension??
            units[k] = 'kPa'
        elif 'EZO_DO' == tag:
            dp = tuple(v/32e-3 for v in dp)
            units[k] = 'uM'

        title_strs.append('{}, current = {:.2f} {}'.format(tag,dp[-1],units[k]))
        
        tmp = zip(ts,dp)
        tmp = json.dumps(tmp,separators=(',',':'))
        data.append(tmp)
    else:
        data.append([])

with open('template/index.html','r') as f:
    template = Template(f.read())
htmlstr = template.render(PLOTS=zip(title_strs,dbtags,units,linecolors,data))
print htmlstr

