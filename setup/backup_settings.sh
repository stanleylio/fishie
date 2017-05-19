#!/bin/bash

DIR="./backup"

if ! [ -e "$DIR" ]
then
	mkdir $DIR
fi

sudo rsync -avh /etc/apache2 $DIR
sudo rsync -avh /etc/supervisor $DIR
sudo rsync -avh /etc/logrotate.d $DIR
sudo rsync -avh /etc/rsnapshot $DIR
sudo rsync -avh /etc/cron.d $DIR
sudo rsync -avh /etc/rabbitmq $DIR
sudo rsync -avh /var/lib/connman $DIR
sudo rsync -avh /etc/wpa_supplicant $DIR

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
