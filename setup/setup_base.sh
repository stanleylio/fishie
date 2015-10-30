#!/bin/bash

NODE_TAG="base-004"
LOGGER_DIR="/home/nuc/node"
SETUP_DIR="/home/nuc/node/setup"


echo "Creating folders"
mkdir -p $LOGGER_DIR


#passwd

# enable serial port access for user nuc
sudo usermod -a -G dialout nuc


echo "Setting hostname"
sudo echo $NODE_TAG > /etc/hostname
sudo echo "127.0.0.1       $NODE_TAG" >> /etc/hosts


sudo apt-get update


echo "Setting system clock and timezone"
#dpkg-reconfigure tzdata
sudo apt-get install ntp -y


# Le boeuf
echo "git init"
sudo apt-get install git -y
#git clone https://github.com/stanleylio/fishie.git $LOGGER_DIR
git clone git@github.com:stanleylio/fishie.git $LOGGER_DIR

cd $LOGGER_DIR
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
git remote set-url origin git@github.com:stanleylio/fishie.git
cd $SETUP_DIR


# Install Python libaries
echo "Installing Python libraries"
sudo apt-get install sqlite3 minicom w3m -y
sudo apt-get install build-essential python-dev python-setuptools -y
sudo apt-get install python-pip python-smbus python-scipy -y
sudo pip install --upgrade setuptools
sudo pip install tzlocal pytz pyserial numpy python-dateutil pyparsing six
sudo pip install numpy --force-reinstall --upgrade
#sudo python -m pip install --upgrade numpy
#sudo pip install -U --force-reinstall scipy --upgrade
#pip install Adafruit_BBIO

sudo apt-get build-dep python-matplotlib -y
#sudo apt-get install libpng-dev -y
#sudo apt-get install libfreetype6-dev -y
#sudo ln -s /usr/local/opt/freetype/include/freetype2 /usr/local/include/freetype

# matplotlib
#git clone git://github.com/matplotlib/matplotlib.git
echo "Getting matplotlib plotting library"
#wget http://softlayer-dal.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
if [ ! -f matplotlib-1.4.3.tar.gz ]; then
    wget http://skylineservers.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
fi
tar -xvzf matplotlib-1.4.3.tar.gz
cd matplotlib-1.4.3
sudo python setup.py install
cd ..
sudo rm -r matplotlib-1.4.3
sudo rm matplotlib-1.4.3.tar.gz

