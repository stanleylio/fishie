#!/bin/bash

cd $HOME/node/display

# - - - - -
# static plots (raw)
# - - - - -
echo "PoH"
python3 t0.py --site=poh
#echo "SF"
#python t0.py --site=sf
echo "Coconut"
python3 t0.py --site=coconut
echo "Makai Pier"
python3 t0.py --site=makaipier
echo "Molokai"
python3 t0.py --site=molokai
echo "Nomilo"
python3 t0.py --site=nomilo
echo "Waikalua"
python3 t0.py --site=waikalua
echo "SMART"
python3 t0.py --site=smart
echo "Lyon"
python3 t0.py --site=lyon
echo "Mokauea"
python3 t0.py --site=mokauea
echo "Mobile/Other"
python3 t0.py --site=uhm
echo "Staging/Dev"
python3 t0.py --site=staging


# - - -
# plot filtered and boundary-checked
# clone the database
# wait, I forgot. what are these for?
#echo "PoH boundary-checked"
#rsync -avzhe ssh --progress $HOME/node/www/poh/storage/sensor_data.db* $HOME/node/www/poh/storage/bounded/
# replace out-of-bound values with Null
#python proc.py --site=poh --dbfile=$HOME/node/www/poh/storage/bounded/sensor_data.db
#chmod g+w $HOME/node/www/poh/storage/bounded/sensor_data.db
# plot boundary-checked
#python t0.py --site=poh --dbfile=$HOME/node/www/poh/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/poh/bounded


# - - - - -
# raw plot for Coconut Island tank test (Katie's)
# - - - - -
#echo "Coconut Island (Katie's)"
#python t0.py --site=coconut --dbfile=$HOME/node/www/coconut/storage/sensor_data.db --plot_dir=$HOME/node/www/coconut

#echo "Coconut boundary-checked"
#rsync -avzhe ssh --progress $HOME/node/www/coconut/storage/sensor_data.db* $HOME/node/www/coconut/storage/bounded/
#python proc.py --site=coconut --dbfile=$HOME/node/www/coconut/storage/bounded/sensor_data.db
#python t0.py --site=coconut --dbfile=$HOME/node/www/coconut/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/coconut/bounded


# - - - - -
# raw plot for Hollie's sensors
# The infrasturcture does not support this yet. Hollie broke the
# "one database file per site" assumption
# - - - - -
#echo "Coconut Island (Hollie's)"
#python t0.py --site=coconut --dbfile=$HOME/data/htank/storage/sensor_data.db --plot_dir=$HOME/node/www/coconut

#echo "Coconut boundary-checked"
#rsync -avzhe ssh --progress $HOME/node/www/htank/storage/sensor_data.db* $HOME/node/www/htank/storage/bounded/
#python proc.py --site=coconut --dbfile=$HOME/node/www/htank/storage/bounded/sensor_data.db
#python t0.py --site=coconut --dbfile=$HOME/node/www/htank/storage/bounded/sensor_data.db --plot_dir=$HOME/node/www/htank/bounded

