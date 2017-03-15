#!/bin/bash

# http://linuxconfig.org/passwordless-ssh
#ssh-keygen
#ssh-copy-id hlio@uhunix.hawaii.edu
#ls ~/.ssh/id_rsa.pub
#ssh hlio@uhunix.hawaii.edu

# the parent directory must exist on the server first as rsync won't recreate the entire dir structure

# glazerlab-i7nuc
REMOTE_HOST=128.171.153.115
# otg-met
#REMOTE_HOST=166.122.96.11

BENCHTEST_DIR="$(hostname)@$REMOTE_HOST:/var/uhcm/incoming/$(hostname)"

# path of the rsync binary on the remote machine
REMOTE_RSYNC_PATH=/usr/bin/rsync

rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress /var/uhcm/ $BENCHTEST_DIR/uhcm/
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress /var/log/ $BENCHTEST_DIR/log/
