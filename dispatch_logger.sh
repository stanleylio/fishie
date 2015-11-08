#!/bin/bash

# http://stackoverflow.com/questions/2366693/run-cron-job-only-if-it-isnt-already-running

#mkdir -p "$HOME/tmp"
#PIDFILE="$HOME/tmp/myprogram.pid"
PIDFILE="/tmp/logger.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= | grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
	echo "Already running."
	exit 99
fi

#/path/to/myprogram > $HOME/tmp/myprogram.log &
#/usr/bin/python $HOME/node/sampling.py &
/usr/bin/python $HOME/node/sampling.py >> $HOME/node/log/sampling.py.log 2>&1

echo $! > "${PIDFILE}"
chmod 644 "${PIDFILE}"
