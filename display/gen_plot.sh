#!/bin/bash

cd $HOME/node/display

# - - - - -
# plot raw
#python t0.py --site=poh --dbfile=$HOME/node/storage/sensor_data.db --plot_dir=$HOME/node/www/poh
python t0.py --site=poh --plot_dir=$HOME/node/www/poh

# - - - - -
# plot filtered and boundary-checked
# clone the database
rsync -avzhe ssh --progress $HOME/node/storage/sensor_data.db* $HOME/node/storage/bounded/poh/
# replace out-of-bound values with Null
python proc.py --site=poh --dbfile=$HOME/node/storage/bounded/poh/sensor_data.db
# plot boundary-checked
python t0.py --site=poh --dbfile=$HOME/node/storage/bounded/poh/sensor_data.db --plot_dir=$HOME/node/www/bounded/poh
