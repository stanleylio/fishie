#!/bin/bash

NODE_TAG="base-004"
LOGGER_DIR="~/node"
SETUP_DIR="~/node/setup"


echo "Creating folders"
mkdir -p $LOGGER_DIR


#passwd


echo "Setting hostname"
echo $NODE_TAG > /etc/hostname
echo "127.0.0.1       $NODE_TAG" >> /etc/hosts


apt-get update


echo "Setting system clock and timezone"
#dpkg-reconfigure tzdata
apt-get install ntp -y


# Le boeuf
echo "git init"
sudo apt-get install git -y
git clone https://github.com/stanleylio/fishie.git $LOGGER_DIR


# Install Python libaries
echo "Installing Python libraries"
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus python-scipy w3m sqlite3 minicom -y
pip install --upgrade setuptools
pip install Adafruit_BBIO tzlocal pytz pyserial numpy python-dateutil pyparsing six --force-reinstall --upgrade


# matplotlib
#git clone git://github.com/matplotlib/matplotlib.git
echo "Getting matplotlib plotting library"
#wget http://softlayer-dal.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
wget http://skylineservers.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
tar -xvzf matplotlib-1.4.3.tar.gz
cd matplotlib-1.4.3
python setup.py install
cd ..
rm -r matplotlib-1.4.3
rm matplotlib-1.4.3.tar.gz

