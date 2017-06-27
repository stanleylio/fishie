#!/bin/bash

PLATFORM=bbb
#PLATFORM=rpi
#PLATFORM=nuc

#passwd

#NODE_TAG="base-001"
#sudo echo $NODE_TAG > /etc/hostname
#sudo echo "127.0.0.1       $NODE_TAG" >> /etc/hosts

if [ "$PLATFORM" == bbb ] || [ "$PLATFORM" == rpi ] ; then
	sudo adduser nuc
	sudo usermod -aG sudo nuc
	sudo usermod -aG dialout nuc
	sudo usermod -aG i2c nuc

# logout, reboot, login as nuc, then
	sudo deluser --remove-home debian
	sudo deluser --remove-home pi
fi

# RSA keys
if [ ! -f ~/.ssh/id_rsa ]; then
	su nuc
	ssh-keygen
	cat ~/.ssh/id_rsa.pub
else
	sudo chmod 700 ~/.ssh/id_rsa
fi


sudo apt update && sudo apt upgrade -y
sudo apt install ntp ntpdate git minicom autossh -y --force-yes
#dpkg-reconfigure tzdata
#sudo nano /etc/ntp.conf

#git clone git@github.com:stanleylio/fishie.git ~/node
git clone https://github.com/stanleylio/fishie ~/node
cd ~/node
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
#git remote set-url origin git@github.com:stanleylio/fishie.git
cd

#git clone git@github.com:stanleylio/kmetlog.git ~/kmetlog
git clone https://github.com/stanleylio/kmetlog
cd ~/kmetlog
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
#git remote set-url origin git@github.com:stanleylio/kmetlog.git
cd


# sampling
sudo apt install supervisor -y --force-yes
sudo systemctl enable supervisor
sudo systemctl start supervisor
#sudo update-rc.d supervisor enable
sudo chown nuc:nuc /etc/supervisor/conf.d
sudo apt install build-essential python-dev python-setuptools python-pip python-twisted -y --force-yes
sudo pip install --upgrade setuptools pip
sudo pip install pyserial requests pycrypto
sudo pip install pyzmq


# RabbitMQ
#wget https://github.com/rabbitmq/rabbitmq-server/releases/download/rabbitmq_v3_6_9/rabbitmq-server_3.6.9-1_all.deb
wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server_3.6.9-1_all.deb
sudo dpkg -i rabbitmq-server_3.6.9-1_all.deb
sudo apt -f install -y
sudo dpkg -i rabbitmq-server_3.6.9-1_all.deb
#rm rabbitmq-server_3.6.9-1_all.deb
sudo pip install pika

sudo chown nuc:nuc /etc/rabbitmq/rabbitmq.config

# db
sudo apt install libmysqlclient-dev mysql-server mysql-client python-mysqldb -y --force-yes
#sudo apt install sqlite3 -y

# vis and proc
#sudo apt install python-flask python-autobahn python-virtualenv -y
#sudo apt install python-numpy python-scipy python-matplotlib python-pandas -y


if [ "$PLATFORM" == bbb ] ; then
	sudo echo "cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5,BB-I2C1,BB-I2C2" >> /boot/uEnv.txt
	sudo echo "cape_disable=bone_capemgr.disable_partno=BB-HDMI" >> /boot/uEnv.txt
	sudo pip install Adafruit_BBIO
	sudo apt install i2c-tools python-smbus -y --force-yes
	bash ~/node/setup/time/install_ds1307.sh

	# expand partition to full disk
	cd /opt/scripts/tools/
	git pull
	sudo ./grow_partition.sh
fi


sudo mkdir /var/uhcm
sudo chown nuc:nuc /var/uhcm
mkdir /var/uhcm/log


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
