#!/bin/bash

# http://www.dragonbe.com/2014/01/pdo-sqlite-error-unable-to-open.html

cd /root/node/storage

chgrp www-data sensor_data.db
chgrp www-data sensor_data.db-shm
chgrp www-data sensor_data.db-wal

chmod g+w sensor_data.db
chmod g+w sensor_data.db-wal
chmod g+w sensor_data.db-shm

cd ..
chgrp www-data storage/
chmod g+w storage/

cd
