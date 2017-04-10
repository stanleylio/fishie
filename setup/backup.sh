#!/bin/bash

# backup to glazerlab-e5 :2222

# same IP as glazerlab-i7nuc
REMOTE_HOST=128.171.153.115
REMOTE_DIR="uhcmbackup@$REMOTE_HOST:/var/backups/uhcm/staging/$(hostname)/"

# ~: including the directory itself;
# ~/: content of the directory only.
rsync -avzhe "ssh -p 2222" --progress ~ $REMOTE_DIR
rsync -avzhe "ssh -p 2222" --progress /var/uhcm $REMOTE_DIR
rsync -avzhe "ssh -p 2222" --progress /var/log $REMOTE_DIR
rsync -avzhe "ssh -p 2222" --progress /var/www $REMOTE_DIR

#TODO: mysqldump...
