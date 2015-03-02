#!/bin/bash

crontab -l > crontab.txt
cat /etc/network/interfaces > interfaces.txt
cat /etc/hostname > hostname.txt
cat /etc/hosts > hosts.txt
cat /etc/resolv.conf > resolv.conf.txt
cat /etc/rc.local > rc.local.txt

cat /etc/apache2/ports.conf > ports.conf
cat /etc/apache2/apache2.conf > apache2.conf
cat /etc/apache2/sites-available/default > default.txt
cat /etc/apache2/sites-available/000-default.conf > 000-default.conf
