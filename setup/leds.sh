#!/bin/bash
# turn off the BBB LEDs
clear

cat /sys/class/leds/beaglebone:green:usr0/trigger
cat /sys/class/leds/beaglebone:green:usr1/trigger
cat /sys/class/leds/beaglebone:green:usr2/trigger
cat /sys/class/leds/beaglebone:green:usr3/trigger

cd /sys/class/leds/beaglebone:green:usr0
echo none > trigger
#echo timer > trigger
#echo 1 > delay_on
#echo 20 > delay_off

cd /sys/class/leds/beaglebone:green:usr1
echo none > trigger

cd /sys/class/leds/beaglebone:green:usr2
echo none > trigger

cd /sys/class/leds/beaglebone:green:usr3
echo none > trigger
