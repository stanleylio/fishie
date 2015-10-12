#!/bin/bash

# http://www.dragonbe.com/2014/01/pdo-sqlite-error-unable-to-open.html

# to test:
# http://192.168.1.102/node_config.py?p=latest_sample&id=7

cd ~/node/storage

# this works:
chmod a+w sensor_data.db
chmod a+w sensor_data.db-shm
chmod a+w sensor_data.db-wal

exit 0

# this also works, but only for as long as the -shm and -wal
# persist once they are deleted and recreated by sampling.py
# again, their group ownership return back to that of the user
# executing sampling.py
sudo chgrp www-data sensor_data.db
sudo chgrp www-data sensor_data.db-shm
sudo chgrp www-data sensor_data.db-wal

sudo chmod g+w sensor_data.db
sudo chmod g+w sensor_data.db-shm
sudo chmod g+w sensor_data.db-wal

sudo chgrp www-data .
sudo chmod g+w .

cd
