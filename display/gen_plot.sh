#!/bin/bash

cd $HOME/node/display

# - - - - -
# plot raw
python gen_plot.py --dbfile=$HOME/node/storage/sensor_data.db --plot_dir=$HOME/node/www

# - - - - -
# plot filtered and boundary-checked
# clone the database
rsync -avzhe ssh --progress $HOME/node/storage/sensor_data.db* $HOME/node/storage/bounded/
# replace out-of-bound values with Null
python proc.py --dbfile=$HOME/node/storage/bounded/sensor_data.db
# plot boundary-checked
python gen_plot.py --dbfile=$HOME/node/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/bounded
