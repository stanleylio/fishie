#!/bin/bash


sudo nano /etc/hostname
sudo nano /etc/hosts

USERNAME="nuc"
RABBITMQPASSWORD=""
HOSTNAME="base-XXX"

#sudo bash -c "echo $HOSTNAME > /etc/hostname"
#sudo echo "127.0.0.1       $USERNAME" >> /etc/hosts



sudo adduser $USERNAME
sudo usermod -aG sudo $USERNAME
sudo usermod -aG dialout $USERNAME
sudo usermod -aG i2c $USERNAME
sudo usermod -aG gpio $USERNAME

sudo bash -c "echo \"$USERNAME ALL=(ALL) NOPASSWD:ALL\" > /etc/sudoers.d/$USERNAME"

# reboot, login as USERNAME, then
sudo reboot
sudo userdel -r -f debian
sudo userdel -r -f pi

cd
touch $(hostname)
sudo chmod 400 $(hostname)

if [ ! -f ~/cred.py ]; then
	touch cred.py
	sudo chmod 600 cred.py
fi

sudo mkdir /var/uhcm
sudo chown $USER:$USER /var/uhcm
mkdir /var/uhcm/log


# RSA keys
if [ ! -f ~/.ssh/id_rsa ]; then
	echo "Generating RSA keys..."
	ssh-keygen
	cat ~/.ssh/id_rsa.pub
	cat ~/.ssh/id_rsa
else
	sudo chmod 400 ~/.ssh/id_rsa
fi


sudo apt update && sudo apt upgrade -y
sudo apt install ntp git i2c-tools minicom autossh build-essential python3-pika -y
sudo dpkg-reconfigure tzdata
sudo nano /etc/ntp.conf


cd
git clone https://github.com/stanleylio/fishie ~/node
cd ~/node


# sampling
cd
sudo apt install supervisor -y
sudo systemctl enable supervisor
sudo chown $USER:$USER /etc/supervisor/conf.d

sudo apt install python3-pip sqlite3 -y
python3 -m pip install --upgrade requests pyserial twisted Adafruit_BBIO RPi.GPIO


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
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmq-plugins enable rabbitmq_shovel
sudo rabbitmq-plugins enable rabbitmq_shovel_management
sudo rabbitmqctl add_user $(hostname) $RABBITMQPASSWORD
sudo rabbitmqctl set_permissions $(hostname) ".*" ".*" ".*"
sudo rabbitmqctl set_user_tags $(hostname) administrator
sudo rabbitmqctl delete_user guest
sudo rabbitmqctl list_users
sudo rabbitmqctl list_user_permissions $(hostname)
sudo echo "[]." > /etc/rabbitmq/rabbitmq.config
sudo chmod 664 /etc/rabbitmq/rabbitmq.config
sudo chmod g+w /etc/rabbitmq
sudo usermod -aG rabbitmq $USER
# need to logout and login again for permissions to apply
# and create the corresponding RabbitMQ user on server
# and cred.py, and all the reverse-SSH stuff...


# db
#sudo apt install libmysqlclient-dev -y
#sudo apt install mysql-server mysql-client python-mysqldb sqlite3 -y


# time
#sudo pip install Adafruit_BBIO Adafruit_GPIO
# i2c-tools is needed for python(3) to access i2c without sudo
#sudo apt install python3-smbus -y
#source ~/node/setup/time/install_ds1307.sh


if [ -a /boot/uEnv.txt ]
then
	#sudo echo "cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5,BB-I2C1,BB-I2C2" >> /boot/uEnv.txt
	#sudo echo "cape_disable=bone_capemgr.disable_partno=BB-HDMI" >> /boot/uEnv.txt
	#uboot_overlay_addr0=/lib/firmware/BB-I2C1-00A0.dtbo
	#uboot_overlay_addr1=/lib/firmware/BB-I2C2-00A0.dtbo
	#uboot_overlay_addr2=/lib/firmware/BB-UART1-00A0.dtbo
	#uboot_overlay_addr3=/lib/firmware/BB-UART2-00A0.dtbo
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

