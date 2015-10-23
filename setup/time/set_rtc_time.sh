#!/bin/bash

# run this when a new I2C RTC is installed
# this gets the time via NTP and write to the newly installed RTC

# update the DS1307
ntpdate -b -s -u pool.ntp.org
date

# detect DS1307 on I2C bus
i2cdetect -y -r 1
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device

hwclock --systohc --rtc=/dev/rtc0
hwclock --show -f /dev/rtc0

hwclock --systohc --rtc=/dev/rtc1
hwclock --show -f /dev/rtc1

