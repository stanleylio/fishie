#!/bin/bash

# should only need to run once, ideally
# Stanley Lio, September 2015

# detect DS1307 on I2C bus
echo "Installing external RTC (DS1307/DS3231)..."
i2cdetect -y -r 1
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
hwclock -r -f /dev/rtc1

cat rc.local.txt > /etc/rc.local

# sync NTP time
echo "Getting time via NTP..."
#ntpdate -b -s -u pool.ntp.org
service ntp stop
ntpdate ntp.hawaii.edu
service ntp start
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
cp /root/setup/time/rtc-ds1307.service /lib/systemd/system/rtc-ds1307.service
systemctl enable rtc-ds1307.service
systemctl start rtc-ds1307.service

# shutdown -r now