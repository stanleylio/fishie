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

#reboot
sudo visudo -f /etc/sudoers.d/nuc
#nuc ALL=(ALL) NOPASSWD:ALL


# RSA keys
if [ ! -f ~/.ssh/id_rsa ]; then
	echo "Generating RSA keys..."
	su nuc
	ssh-keygen
	cat ~/.ssh/id_rsa.pub
else
	sudo chmod 700 ~/.ssh/id_rsa
fi


sudo apt update && sudo apt upgrade -y
sudo apt install ntp ntpdate git minicom autossh -y
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
sudo apt install supervisor -y
sudo systemctl enable supervisor
sudo systemctl start supervisor
#sudo update-rc.d supervisor enable
sudo chown nuc:nuc /etc/supervisor/conf.d
sudo apt install build-essential python-dev python-setuptools python-pip python-twisted python-zmq -y
sudo pip install --upgrade setuptools pip
sudo pip install pyserial requests pycrypto
#sudo pip install pyzmq


# RabbitMQ
#wget https://github.com/rabbitmq/rabbitmq-server/releases/download/rabbitmq_v3_6_9/rabbitmq-server_3.6.9-1_all.deb
#wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server_3.6.9-1_all.deb
#wget https://github.com/rabbitmq/rabbitmq-server/releases/download/rabbitmq_v3_6_11/rabbitmq-server_3.6.11-1_all.deb
wget https://github.com/rabbitmq/rabbitmq-server/releases/download/rabbitmq_v3_6_12/rabbitmq-server_3.6.12-1_all.deb
sudo dpkg -i rabbitmq-server_3.6.12-1_all.deb
sudo apt -f install -y
sudo dpkg -i rabbitmq-server_3.6.12-1_all.deb
#sudo rabbitmqctl add_user nuc password here
#sudo rabbitmqctl set_permissions nuc ".*" ".*" ".*"
#sudo rabbitmqctl set_user_tags nuc administrator
#sudo rabbitmqctl list_user_permissions nuc
sudo rabbitmq-plugins enable rabbitmq_management
#sudo rabbitmq-plugins enable rabbitmq_shovel
#sudo rabbitmq-plugins enable rabbitmq_shovel_management
sudo chown nuc:nuc /etc/rabbitmq/rabbitmq.config
sudo pip install pika


# db
#sudo apt install libmysqlclient-dev -y
sudo apt install mysql-server mysql-client python-mysqldb sqlite3 -y


sudo mkdir /var/uhcm
sudo chown nuc:nuc /var/uhcm
mkdir /var/uhcm/log


if [ "$PLATFORM" == bbb ] ; then
	sudo echo "cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5,BB-I2C1,BB-I2C2" >> /boot/uEnv.txt
	sudo echo "cape_disable=bone_capemgr.disable_partno=BB-HDMI" >> /boot/uEnv.txt
	sudo pip install Adafruit_BBIO
	sudo apt install i2c-tools python-smbus -y
	source ~/node/setup/time/install_ds1307.sh

	# expand partition to full disk
	cd /opt/scripts/tools/
	sudo git pull
	sudo ./grow_partition.sh
fi

if [ "$PLATFORM" == rpi ] ; then
	sudo apt install i2c-tools python-smbus -y
	source ~/node/setup/time/install_ds1307.sh
fi
