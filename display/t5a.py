# loko i'a app water depth at makaha1 and 2
#
# Stanley H.I. Lio
# hlio@soest.hawaii.edu
# All Rights Reserved. 2017
import sys,traceback,json,time,requests
from os import makedirs
from os.path import exists,join,expanduser
sys.path.append(expanduser('~'))
from datetime import datetime,timedelta
from node.display.gen_plot import plot_time_series


# makaha 1 weekly
r = requests.get('http://grogdata.soest.hawaii.edu/poh/data/location/makaha1/depth.json?minutes=10080&max_count=1000')
r = r.json()
r['depth_meter'] = [tmp*3.28084 for tmp in r['depth_meter']]
plot_time_series(r['ReceptionTime'],r['depth_meter'],\
                 join('/var/www/uhcm/img/poh/node-009/weekly/depth_feet.png'),\
                 title='Water Depth at Makaha 1 (node-009)',\
                 ylabel='Feet',\
                 linelabel='Water Depth')

# makaha 1 monthly
r = requests.get('http://grogdata.soest.hawaii.edu/poh/data/location/makaha1/depth.json?minutes=43200&max_count=1000')
r = r.json()
r['depth_meter'] = [tmp*3.28084 for tmp in r['depth_meter']]
plot_time_series(r['ReceptionTime'],r['depth_meter'],\
                 join('/var/www/uhcm/img/poh/node-009/monthly/depth_feet.png'),\
                 title='Water Depth at Makaha 1 (node-009)',\
                 ylabel='Feet',\
                 linelabel='Water Depth')

# makaha 2 weekly
r = requests.get('http://grogdata.soest.hawaii.edu/poh/data/location/makaha2/depth.json?minutes=10080&max_count=1000')
r = r.json()
r['depth_meter'] = [tmp*3.28084 for tmp in r['depth_meter']]
plot_time_series(r['ReceptionTime'],r['depth_meter'],\
                 join('/var/www/uhcm/img/poh/node-008/weekly/depth_feet.png'),\
                 title='Water Depth at Makaha 2 (node-008)',\
                 ylabel='Feet',\
                 linelabel='Water Depth')

# makaha 2 monthly
r = requests.get('http://grogdata.soest.hawaii.edu/poh/data/location/makaha2/depth.json?minutes=43200&max_count=1000')
r = r.json()
r['depth_meter'] = [tmp*3.28084 for tmp in r['depth_meter']]
plot_time_series(r['ReceptionTime'],r['depth_meter'],\
                 join('/var/www/uhcm/img/poh/node-008/monthly/depth_feet.png'),\
                 title='Water Depth at Makaha 2 (node-008)',\
                 ylabel='Feet',\
                 linelabel='Water Depth')

