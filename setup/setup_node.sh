#!/bin/bash

NODE_TAG="node-011"
LOGGER_DIR="~/node"
SETUP_DIR="~/node/setup"


passwd
ssh-keygen
cat ~/.ssh/id_rsa.pub


echo "Setting hostname"
echo $NODE_TAG > /etc/hostname
echo "127.0.0.1       $NODE_TAG" >> /etc/hosts

sudo apt update
sudo apt upgrade

sudo apt install git supervisor i2c-tools minicom -y
#sudo apt install ntpdate -y

echo "Setting system clock, timezone and RTC"
#date -s "10 SEP 2015 22:00:30"
# Debian default to UTC - no change required
sudo dpkg-reconfigure tzdata
#sudo apt-get install ntp -y
# RTC
#echo "Reading system clock and RTC"
echo "(must be done manually if NTP is not available)"
bash $SETUP_DIR/time/install_ds1307.sh


# Le boeuf
echo "git init"
git clone https://github.com/stanleylio/fishie.git $LOGGER_DIR
cd $LOGGER_DIR
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
git remote set-url origin git@github.com:stanleylio/fishie.git
cd

# ... coz the first time it ran without node/setup/time/install_ds1307.sh
# yet it still need the correct time to git clone
bash $SETUP_DIR/time/install_ds1307.sh


# Install Python libaries
echo "Installing Python libraries"
sudo apt install build-essential python-dev python-setuptools python-pip -y
sudo apt install python-smbus sqlite3 -y
sudo pip install --upgrade pip setuptools
sudo pip install Adafruit_BBIO pyserial
#sudo apt install python-scipy w3m -y
#sudo pip install six tzlocal pytz numpy python-dateutil pyparsing --force-reinstall --upgrade
#sudo pip install requests
#sudo pip install six tzlocal pytz numpy python-dateutil pyparsing --upgrade

#numpy, matplotlib...

pip install pyzmq sqlalchemy requests pycrypto
sudo apt install python-flask python-autobahn python-virtualenv -y

git clone -b trunk https://github.com/twisted/twisted.git
cd twisted
sudo python setup.py install
cd

git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
cd


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


#sudo apt-get dist-upgrade -y


bash $SETUP_DIR/disable_services.sh
#bash setup_server.sh


# expand partition to full disk
cd /opt/scripts/tools/
git pull
sudo ./grow_partition.sh
#shutdown -r now

