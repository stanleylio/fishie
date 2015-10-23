#!/bin/bash

i2cdetect -l
echo BB-I2C1 > /sys/devices/bone_capemgr.9/slots
cat /sys/devices/bone_capemgr.9/slots
i2cdetect -l
