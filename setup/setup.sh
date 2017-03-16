#!/bin/bash

NODE_TAG="base-004"
SETUP_DIR="~/node/setup"

#passwd

#sudo echo $NODE_TAG > /etc/hostname
#sudo echo "127.0.0.1       $NODE_TAG" >> /etc/hosts

#ssh-keygen
#cat ~/.ssh/id_rsa.pub

# enable serial port access for user
#sudo usermod -a -G dialout nuc


sudo apt update
sudo apt upgrade


sudo apt install ntp ntpdate -y
#dpkg-reconfigure tzdata

sudo apt install git -y
cd
git clone git@github.com:stanleylio/fishie.git node
cd node
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
#git remote set-url origin git@github.com:stanleylio/fishie.git
cd

cd
git clone git@github.com:stanleylio/kmetlog.git ~/kmetlog
cd kmetlog
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
cd


# sampling
sudo apt install supervisor -y
sudo update-rc.d supervisor enable
sudo apt install build-essential python-dev python-setuptools python-pip -y
sudo apt install python-twisted -y
sudo pip install --upgrade setuptools pip
sudo pip install pyserial
sudo pip install pyzmq requests pycrypto

# db
#sudo apt install libmysqlclient-dev mysql-server mysql-client python-mysqldb -y
sudo apt install sqlite3 -y

# debugging
sudo apt install minicom autossh -y

# vis and proc
#sudo apt install python-flask python-autobahn python-virtualenv -y
#sudo apt install python-numpy python-scipy python-matplotlib python-pandas -y

# bbb-based
if ! [ -a /boot/uEnv.txt ];
then
	exit 0;
fi




echo "install bone stuff?"
pause
sudo echo "cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5,BB-I2C1,BB-I2C2" >> /boot/uEnv.txt
#sudo pip install Adafruit_BBIO
sudo apt install i2c-tools python-smbus -y
bash $SETUP_DIR/time/install_ds1307.sh


# disable the HDMI cape to save power
# http://wiki.beyondlogic.org/index.php?title=BeagleBoneBlack_Cape_Manager
#sudo cat /sys/devices/bone_capemgr.*/slots
#sudo mkdir /media/card
#sudo mount /dev/mmcblk0p1 /media/card
#echo "now add this line to /media/card/uEnv.txt:"
#echo "optargs=quiet capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN"
#sudo nano /media/card/uEnv.txt

bash $SETUP_DIR/disable_services.sh

# expand partition to full disk
cd /opt/scripts/tools/
git pull
sudo ./grow_partition.sh
#sudo reboot


#sudo apt install libblas-dev liblapack-dev gfortran
#sudo apt install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
#sudo pip install tzlocal pytz python-dateutil pyparsing six --force-reinstall --upgrade
# still can't import? try these in python
#import numpy
#print numpy.__path__
# and delete that dir

#sudo apt-get build-dep python-matplotlib -y
#sudo ln -s /usr/local/opt/freetype/include/freetype2 /usr/local/include/freetype

# matplotlib
#git clone git://github.com/matplotlib/matplotlib.git
#echo "Getting matplotlib plotting library"
#wget http://softlayer-dal.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
#if [ ! -f matplotlib-1.4.3.tar.gz ]; then
#    wget http://skylineservers.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz
#fi
#tar -xvzf matplotlib-1.4.3.tar.gz
#cd matplotlib-1.4.3
#sudo python setup.py install
#cd ..
#sudo rm -r matplotlib-1.4.3
#sudo rm matplotlib-1.4.3.tar.gz
