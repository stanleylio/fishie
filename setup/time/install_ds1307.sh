#!/bin/bash
# Only need to run once to setup new device
# Stanley H.I. Lio
# 2017

echo "Installing external RTC (DS1307/DS3231)..."
# pi
echo "Installing external RTC (DS1307/DS3231)..."
if [ -f /sys/class/i2c-adapter/i2c-1 ]; then
	sudo i2cdetect -y -r 1
	echo "using i2c-1"
	sudo bash -c "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device"
fi
# bone
if [ -f /sys/class/i2c-adapter/i2c-2 ]; then
	sudo i2cdetect -y -r 2
	echo "using i2c-2"
	sudo bash -c "echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-2/new_device"
fi
sudo hwclock -r -f /dev/rtc1


#date -s "10 SEP 2015 22:00:30"

# sync NTP time
echo "Getting time via NTP..."
#sudo echo "server ntp.soest.hawaii.edu" >> /etc/ntp.conf
sudo systemctl stop ntp
sudo ntpd -gq
sudo systemctl start ntp
date
#sudo timedatectl

# write to RTC
if [ "$PLATFORM" == bbb ] ; then
	echo "Setting internal RTC..."
	sudo hwclock --systohc --rtc=/dev/rtc0
	sudo hwclock --show -f /dev/rtc0

	echo "Setting external rtc..."
	sudo hwclock --systohc --rtc=/dev/rtc1
	sudo hwclock --show --rtc=/dev/rtc1
fi

#chmod +x clock_init.sh

echo "Installing service..."
sudo cp /home/nuc/node/setup/time/rtc-ds1307.service /lib/systemd/system/rtc-ds1307.service
sudo systemctl enable rtc-ds1307.service
sudo systemctl start rtc-ds1307.service
