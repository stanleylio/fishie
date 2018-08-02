#!/bin/bash


sudo nano /etc/hostname
sudo nano /etc/hosts

USERNAME="nuc"
RABBITMQPASSWORD=
#HOSTNAME="base-XXX"

#sudo bash -c "echo $HOSTNAME > /etc/hostname"
#sudo echo "127.0.0.1       $USERNAME" >> /etc/hosts

sudo adduser $USERNAME
sudo usermod -aG sudo $USERNAME
sudo usermod -aG dialout $USERNAME
sudo usermod -aG i2c $USERNAME
sudo usermod -aG gpio $USERNAME
#sudo adduser pi gpio

# reboot, login as USERNAME, then
sudo bash -c "echo \"$USER ALL=(ALL) NOPASSWD:ALL\" > /etc/sudoers.d/$USER"
sudo userdel -r -f debian
sudo userdel -r -f pi


# RSA keys
if [ ! -f ~/.ssh/id_rsa ]; then
	echo "Generating RSA keys..."
	ssh-keygen
	cat ~/.ssh/id_rsa.pub
else
	sudo chmod 400 ~/.ssh/id_rsa
fi


sudo apt update && sudo apt upgrade -y
sudo apt install ntp ntpdate git minicom autossh bash-completion -y
#dpkg-reconfigure tzdata
#sudo nano /etc/ntp.conf


cd
#git clone git@github.com:stanleylio/fishie.git ~/node
git clone https://github.com/stanleylio/fishie ~/node
cd ~/node
git config --global user.name "Stanley Lio"
git config --global user.email stanleylio@gmail.com
#git remote set-url origin git@github.com:stanleylio/fishie.git

#cd
#git clone git@github.com:stanleylio/kmetlog.git ~/kmetlog
#git clone https://github.com/stanleylio/kmetlog
#cd ~/kmetlog
#git config --global user.name "Stanley Lio"
#git config --global user.email stanleylio@gmail.com
#git remote set-url origin git@github.com:stanleylio/kmetlog.git


# sampling
cd
sudo apt install supervisor -y
sudo systemctl enable supervisor
sudo systemctl start supervisor
sudo chown $USER:$USER /etc/supervisor/conf.d
#sudo apt install build-essential python-dev python-setuptools python-pip python-twisted python-zmq -y
#sudo pip install --upgrade pyserial requests pycrypto pika
sudo apt install python3 python3-pip python3-scipy python3-smbus -y
sudo pip3 install --upgrade pika requests pycrypto pyserial pyzmq twisted Adafruit_BBIO Adafruit_GPIO RPi.GPIO


# RabbitMQ
cd
# For the Pi:
#wget http://packages.erlang-solutions.com/site/esl/esl-erlang/FLAVOUR_1_general/esl-erlang_20.1.7-1~raspbian~stretch_armhf.deb
#sudo dpkg -i esl-erlang_20.1.7-1~raspbian~stretch_armhf.deb
#sudo apt -f install -y
#wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.0/rabbitmq-server_3.7.0-1_all.deb
#sudo dpkg -i rabbitmq-server_3.7.0-1_all.deb
#sudo apt -f install -y
#sudo dpkg -i rabbitmq-server_3.7.0-1_all.deb

# follow these instead:
#https://www.rabbitmq.com/install-debian.html
#https://packages.erlang-solutions.com/erlang/#tabs-debian

sudo apt install rabbitmq-server -y
sudo rabbitmqctl add_user $(hostname) $RABBITMQPASSWORD
sudo rabbitmqctl set_permissions $(hostname) ".*" ".*" ".*"
sudo rabbitmqctl set_user_tags $(hostname) administrator
sudo rabbitmqctl delete_user guest
sudo rabbitmqctl list_users
sudo rabbitmqctl list_user_permissions $(hostname)
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmq-plugins enable rabbitmq_shovel
sudo rabbitmq-plugins enable rabbitmq_shovel_management
#sudo nano /etc/rabbitmq/rabbitmq.config
#sudo chmod 664 /etc/rabbitmq/rabbitmq.config
#sudo chmod g+w /etc/rabbitmq
#sudo usermod -aG rabbitmq $USER
# need to logout and login again for permissions to apply
#sudo nano /etc/rabbitmq/rabbitmq.config
# and create the corresponding RabbitMQ user on server

# and cred.py, and all the reverse-SSH stuff...


# db
#sudo apt install libmysqlclient-dev -y
#sudo apt install mysql-server mysql-client python-mysqldb sqlite3 -y
sudo apt install sqlite3 -y


sudo mkdir /var/uhcm
sudo chown $USER:$USER /var/uhcm
mkdir /var/uhcm/log

#sudo pip install Adafruit_BBIO Adafruit_GPIO
# i2c-tools is needed for python(3) to access i2c without sudo
sudo apt install i2c-tools -y
#sudo apt install python3-smbus -y
source ~/node/setup/time/install_ds1307.sh


if [ -a /boot/uEnv.txt ]
then
	#sudo echo "cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5,BB-I2C1,BB-I2C2" >> /boot/uEnv.txt
	#sudo echo "cape_disable=bone_capemgr.disable_partno=BB-HDMI" >> /boot/uEnv.txt
	###Overide capes with eeprom
	#uboot_overlay_addr0=/lib/firmware/BB-I2C1-00A0.dtbo
	#uboot_overlay_addr1=/lib/firmware/BB-I2C2-00A0.dtbo
	#uboot_overlay_addr2=/lib/firmware/BB-UART1-00A0.dtbo
	#uboot_overlay_addr3=/lib/firmware/BB-UART2-00A0.dtbo
	###
	###Additional custom capes
	#uboot_overlay_addr4=/lib/firmware/BB-UART4-00A0.dtbo
	#uboot_overlay_addr5=/lib/firmware/BB-UART5-00A0.dtbo
	sudo nano /boot/uEnv.txt
fi


if [ -e "/opt/scripts/tools" ]
then
	# expand partition to full disk
	cd /opt/scripts/tools
	sudo git pull
	sudo ./grow_partition.sh
fi

# reboot, then bash ~/node/setup/time/install_ds1307.sh

# if on beaglebone, change log rotate frequency: sudo nano /etc/logrotate.d/rabbitmq-server

