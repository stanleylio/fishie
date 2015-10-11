#!/bin/bash

# http://www.dragonbe.com/2014/01/pdo-sqlite-error-unable-to-open.html

# to test:
# http://192.168.1.102/node_config.py?p=latest_sample&id=7

cd ~/node/storage

sudo chgrp www-data sensor_data.db
sudo chgrp www-data sensor_data.db-shm
sudo chgrp www-data sensor_data.db-wal

sudo chmod g+w sensor_data.db
sudo chmod g+w sensor_data.db-shm
sudo chmod g+w sensor_data.db-wal

cd ..
sudo chgrp www-data storage/
sudo chmod g+w storage/

cd
