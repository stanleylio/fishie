#!/bin/bash
# schedule this to run on boot to set system clock using the DS1307 RTC

sleep 1

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


# for debugging
#log="/root/ds1307.txt"
#log="/root/setup/time/clock_init.log"
#date


# from external RTC to system time
if [ -e /dev/rtc0 ]; then
	echo "rtc0:"
	sudo hwclock -r -f /dev/rtc0
	sudo hwclock --hctosys -f /dev/rtc0
fi
if [ -e /dev/rtc1 ]; then
	echo "rtc1:"
	sudo hwclock -r -f /dev/rtc1
	sudo hwclock --hctosys -f /dev/rtc1
fi

# from system time to internal rtc
sudo hwclock --systohc -f /dev/rtc0

exit 0
