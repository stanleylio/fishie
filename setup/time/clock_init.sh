#!/bin/bash
# schedule this to run on boot to set system clock using the DS1307 RTC

sleep 2

#echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
if [ -f /sys/class/i2c-adapter/i2c-1 ]; then
	i2cdetect -y -r 1
	echo "using i2c-1"
	echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
fi
if [ -f /sys/class/i2c-adapter/i2c-2 ]; then
	i2cdetect -y -r 2
	echo "using i2c-2"
	echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-2/new_device
fi


# for debugging
#log="/root/ds1307.txt"
#log="/root/setup/time/clock_init.log"

date

echo "rtc0 (bbb):"
hwclock --show -f /dev/rtc0

echo "rtc1 (ds1307/ds3231):"
hwclock --show -f /dev/rtc1

# from DS1307 to system time
hwclock --hctosys -f /dev/rtc1

# from system time to BBB's rtc
hwclock --systohc -f /dev/rtc0
