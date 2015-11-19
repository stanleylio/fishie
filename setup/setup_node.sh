#!/bin/bash

NODE_TAG="node-007"
LOGGER_DIR="/root/node"
SETUP_DIR="/root/node/setup"

#echo "Creating folders"
#mkdir -p $LOGGER_DIR

passwd

echo "Setting hostname"
echo $NODE_TAG > /etc/hostname
echo "127.0.0.1       $NODE_TAG" >> /etc/hosts


sudo apt-get update

#sudo apt-get install supervisor -y
sudo apt-get install rcconf i2c-tools ntpdate -y



echo "Setting system clock, timezone and RTC"
#date -s "10 SEP 2015 22:00:30"
# Debian default to UTC - no change required
dpkg-reconfigure tzdata
#sudo apt-get install ntp -y
# RTC
#echo "Reading system clock and RTC"
echo "(must be done manually if NTP is not available)"
bash ./time/install_ds1307.sh


# Le boeuf
echo "git init"
sudo apt-get install git -y
git clone https://github.com/stanleylio/fishie.git $LOGGER_DIR


# ... coz the first time it ran without node/setup/time/install_ds1307.sh
# yet it still need the correct time to git clone
bash ./time/install_ds1307.sh


# Install Python libaries
echo "Installing Python libraries"
sudo apt-get install build-essential python-dev python-setuptools python-pip -y
sudo apt-get install sqlite3 minicom python-smbus python-scipy w3m -y
pip install --upgrade setuptools
pip install Adafruit_BBIO pyserial
pip install six tzlocal pytz numpy python-dateutil pyparsing --force-reinstall --upgrade


# matplotlib
#git clone git://github.com/matplotlib/matplotlib.git
#echo "Getting matplotlib plotting library"
#wget http://softlayer-dal.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
#wget http://skylineservers.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
#tar -xvzf matplotlib-1.4.3.tar.gz
#cd matplotlib-1.4.3
#sudo python setup.py install
#cd ..
#rm -r matplotlib-1.4.3
#rm matplotlib-1.4.3.tar.gz


# disable the HDMI cape to save power
# http://wiki.beyondlogic.org/index.php?title=BeagleBoneBlack_Cape_Manager
sudo cat /sys/devices/bone_capemgr.*/slots
sudo mkdir /media/card
sudo mount /dev/mmcblk0p1 /media/card
echo "now add this line to /media/card/uEnv.txt:"
echo "optargs=quiet capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN"
sudo nano /media/card/uEnv.txt


sudo apt-get dist-upgrade -y


bash disable_services.sh
#bash setup_server.sh


# expand partition to full disk
cd /opt/scripts/tools/
git pull
sudo ./grow_partition.sh
#shutdown -r now

