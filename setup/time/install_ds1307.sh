#!/bin/bash

# should only need to run once
# on newer bbb distribution where root is disabled, sudo -s first
# Stanley H.I. Lio, 2017

# detect RTC on I2C bus
echo "Installing external RTC (DS1307/DS3231)..."
#if [ -f /sys/class/i2c-adapter/i2c-1 ]; then
#	i2cdetect -y -r 1
#	echo "using i2c-1"
#	echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
#fi
if [ -f /sys/class/i2c-adapter/i2c-2 ]; then
	i2cdetect -y -r 2
	echo "using i2c-2"
	echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-2/new_device
fi
hwclock -r -f /dev/rtc1

#cat rc.local.txt > /etc/rc.local

# sync NTP time
echo "Getting time via NTP..."
#ntpdate -b -s -u pool.ntp.org
#ntpdate ntp.soest.hawaii.edu
#sudo service ntp stop
sudo systemctl stop ntp
ntpd -gq
#sudo service ntp start
sudo systemctl start ntp
#date -s "10 SEP 2015 22:00:30"
date
#timedatectl

# write to RTC
echo "Setting BBB rtc..."
hwclock --systohc --rtc=/dev/rtc0
hwclock --show -f /dev/rtc0

echo "Setting external rtc..."
hwclock --systohc --rtc=/dev/rtc1
hwclock --show --rtc=/dev/rtc1

#chmod +x clock_init.sh

echo "Installing service..."
cp ~/node/setup/time/rtc-ds1307.service /lib/systemd/system/rtc-ds1307.service
cp /home/nuc/node/setup/time/rtc-ds1307.service /lib/systemd/system/rtc-ds1307.service
systemctl enable rtc-ds1307.service
systemctl start rtc-ds1307.service
#cp ~/node/setup/time/rtc-ds1307.service /lib/systemd/system/rtc-ds1307_rpi2.service
#systemctl enable rtc-ds1307_rpi2.service
#systemctl start rtc-ds1307_rpi2.service

# shutdown -r now
exit 0
