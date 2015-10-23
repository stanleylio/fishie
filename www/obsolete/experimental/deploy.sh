#!/bin/bash

LOGGER_DIR="/root/node"

chmod o+x gen_var_page.py

ln $LOGGER_DIR/storage/sensor_data.db
ln $LOGGER_DIR/storage/sensor_data.db-shm
ln $LOGGER_DIR/storage/sensor_data.db-wal

chmod o+w sensor_data.db
chmod o+w sensor_data.db-shm
chmod o+w sensor_data.db-wal

ln $LOGGER_DIR/storage/storage.py
ln $LOGGER_DIR/config_support.py

ln $LOGGER_DIR/display_config.ini
ln $LOGGER_DIR/node_config.ini

