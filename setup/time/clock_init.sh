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

date

echo "rtc0 (internal):"
hwclock --show -f /dev/rtc0

echo "rtc1 (ds1307/ds3231):"
hwclock --show -f /dev/rtc1

# from external RTC to system time
if [ -f /dev/rtc0 ]; then
	sudo hwclock --hctosys -f /dev/rtc0
fi
if [ -f /dev/rtc1 ]; then
	sudo hwclock --hctosys -f /dev/rtc1
fi

# from system time to internal rtc
hwclock --systohc -f /dev/rtc0

exit 0
