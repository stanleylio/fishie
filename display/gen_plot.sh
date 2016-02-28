#!/bin/bash

cd $HOME/node/display

# - - - - -
# plot raw
python t0.py --site=poh --dbfile=$HOME/node/www/poh/storage/sensor_data.db --plot_dir=$HOME/node/www/poh

#rsync -avh $HOME/node/www/poh $HOME/cm1app/cm1app/static/

# - - - - -
# plot filtered and boundary-checked
# clone the database
rsync -avzhe ssh --progress $HOME/node/www/poh/storage/sensor_data.db* $HOME/node/www/poh/storage/bounded/
# replace out-of-bound values with Null
python proc.py --site=poh --dbfile=$HOME/node/www/poh/storage/bounded/sensor_data.db
# plot boundary-checked
python t0.py --site=poh --dbfile=$HOME/node/www/poh/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/poh/bounded
