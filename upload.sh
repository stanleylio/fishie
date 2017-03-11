#!/bin/bash

# http://linuxconfig.org/passwordless-ssh
#ssh-keygen
#ssh-copy-id hlio@uhunix.hawaii.edu
#ls ~/.ssh/id_rsa.pub
#ssh hlio@uhunix.hawaii.edu

# the parent directory must already exists on the server as rsync won't recreate the entire dir structure

# glazerlab-i7nuc
#RemoteHost=128.171.153.115
# otg-met
REMOTE_HOST=166.122.96.11

REMOTE_DIR="$(hostname)@$REMOTE_HOST:/var/kmetlog/incoming/$(hostname)"

# path of the rsync binary on the remote machine
REMOTE_RSYNC_PATH=/usr/bin/rsync

rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress /var/kmetlog/ $REMOTE_DIR/kmetlog/
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress /var/log/ $REMOTE_DIR/log/
