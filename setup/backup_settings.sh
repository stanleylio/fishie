#!/bin/bash

DIR="./backup"

if ! [ -e "$DIR" ]
then
	mkdir $DIR
fi

sudo rsync -avh --delete /etc/apache2 $DIR
sudo rsync -avh --delete /etc/supervisor $DIR
sudo rsync -avh --delete /etc/logrotate.d $DIR
sudo rsync -avh --delete /etc/cron.d $DIR
sudo rsync -avh --delete /etc/rabbitmq $DIR
sudo rsync -avh --delete /etc/wpa_supplicant $DIR
if [ -e "/var/lib/connman" ]
then
	sudo rsync -avh --delete /var/lib/connman $DIR
fi
if [ -e "/etc/rsnapshot" ]
then
	sudo rsync -avh --delete /etc/rsnapshot $DIR
fi

crontab -l > $DIR/crontab.txt
cp /etc/fstab $DIR/fstab
if [ -a /boot/uEnv.txt ]
then
	cp /boot/uEnv.txt $DIR/uEnv.txt
fi
cp -a /etc/network/interfaces $DIR/interfaces.txt
cp -a /etc/hostname $DIR/hostname.txt
cp -a /etc/hosts $DIR/hosts.txt
#cp -a /etc/resolv.conf $DIR/resolv.conf.txt
cat /etc/resolv.conf > $DIR/resolv.conf.txt
cp -a /etc/rc.local $DIR/rc.local.txt
cp -a /etc/ntp.conf $DIR/ntp.conf
#pip freeze > $DIR/pipfreeze.txt
#pip3 freeze > $DIR/pip3freeze.txt
