#!/bin/bash
# enable the other I2C port on the BBB

i2cdetect -l
#echo BB-I2C1 > /sys/devices/bone_capemgr.9/slots
echo BB-I2C1 > /sys/devices/platform/bone_capemgr/slots
cat /sys/devices/platform/bone_capemgr/slots
i2cdetect -l
