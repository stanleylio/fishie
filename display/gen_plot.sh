#!/bin/bash

cd $HOME/node/display

# - - - - -
# raw plot for PoH
# - - - - -
echo "PoH"
python t0.py --site=poh --dbfile=$HOME/node/www/poh/storage/sensor_data.db --plot_dir=$HOME/node/www/poh

#rsync -avh $HOME/node/www/poh $HOME/cm1app/cm1app/static/

# - - -
# plot filtered and boundary-checked
# clone the database
# wait, I forgot. what are these for?
echo "PoH boundary-checked"
rsync -avzhe ssh --progress $HOME/node/www/poh/storage/sensor_data.db* $HOME/node/www/poh/storage/bounded/
# replace out-of-bound values with Null
python proc.py --site=poh --dbfile=$HOME/node/www/poh/storage/bounded/sensor_data.db
# plot boundary-checked
python t0.py --site=poh --dbfile=$HOME/node/www/poh/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/poh/bounded


# - - - - -
# raw plot for Coconut Island tank test
# - - - - -
echo "Coconut Island"
python t0.py --site=coconut --dbfile=$HOME/node/www/coconut/storage/sensor_data.db --plot_dir=$HOME/node/www/coconut

echo "Coconut boundary-checked"
rsync -avzhe ssh --progress $HOME/node/www/coconut/storage/sensor_data.db* $HOME/node/www/coconut/storage/bounded/
python proc.py --site=coconut --dbfile=$HOME/node/www/coconut/storage/bounded/sensor_data.db
python t0.py --site=coconut --dbfile=$HOME/node/www/coconut/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/coconut/bounded


