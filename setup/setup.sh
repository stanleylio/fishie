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

# reboot, login as nuc, then
sudo bash -c "echo \"$USERNAME ALL=(ALL) NOPASSWD:ALL\" > /etc/sudoers.d/$USERNAME"
sudo userdel -r -f debian
sudo userdel -r -f pi


# RSA keys
if [ ! -f ~/.ssh/id_rsa ]; then
	echo "Generating RSA keys..."
	ssh-keygen
	cat ~/.ssh/id_rsa.pub
else
	sudo chmod 700 ~/.ssh/id_rsa
fi


sudo apt update && sudo apt upgrade -y
sudo apt install ntp ntpdate git minicom autossh -y
#dpkg-reconfigure tzdata
#sudo nano /etc/ntp.conf


cd
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


# sampling
cd
sudo apt install supervisor -y
sudo systemctl enable supervisor
sudo systemctl start supervisor
sudo chown $USERNAME:$USERNAME /etc/supervisor/conf.d
sudo apt install build-essential python-dev python-setuptools python-pip python-twisted python-zmq -y
sudo pip install --upgrade pyserial requests pycrypto pika
sudo apt install python3 python3-pip -y
sudo pip3 install --upgrade pika requests twisted Adafruit_BBIO Adafruit_GPIO


# RabbitMQ
cd
wget https://github.com/rabbitmq/rabbitmq-server/releases/download/rabbitmq_v3_6_12/rabbitmq-server_3.6.12-1_all.deb
sudo dpkg -i rabbitmq-server_3.6.12-1_all.deb
sudo apt -f install -y
sudo dpkg -i rabbitmq-server_3.6.12-1_all.deb
sudo rabbitmqctl add_user $(hostname) $RABBITMQPASSWORD
sudo rabbitmqctl set_permissions $(hostname) ".*" ".*" ".*"
sudo rabbitmqctl set_user_tags $(hostname) administrator
sudo rabbitmqctl delete_user guest
sudo rabbitmqctl list_users
sudo rabbitmqctl list_user_permissions $(hostname)
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmq-plugins enable rabbitmq_shovel
sudo rabbitmq-plugins enable rabbitmq_shovel_management
#sudo touch /etc/rabbitmq/rabbitmq.config
#sudo chmod 664 /etc/rabbitmq/rabbitmq.config
sudo chmod g+w /etc/rabbitmq
sudo usermod -aG rabbitmq $USERNAME
sudo nano /etc/rabbitmq/rabbitmq.config
# and create the corresponding RabbitMQ user on server

# and cred.py, and all the reverse-SSH stuff...


# db
#sudo apt install libmysqlclient-dev -y
#sudo apt install mysql-server mysql-client python-mysqldb sqlite3 -y
sudo apt install sqlite3 -y


sudo mkdir /var/uhcm
sudo chown $USERNAME:$USERNAME /var/uhcm
mkdir /var/uhcm/log

sudo pip install Adafruit_BBIO Adafruit_GPIO
sudo apt install i2c-tools python-smbus -y
source ~/node/setup/time/install_ds1307.sh


if [ -a /boot/uEnv.txt ]
then
	#sudo echo "cape_enable=bone_capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5,BB-I2C1,BB-I2C2" >> /boot/uEnv.txt
	#sudo echo "cape_disable=bone_capemgr.disable_partno=BB-HDMI" >> /boot/uEnv.txt
	sudo nano /boot/uEnv.txt
fi


if [ -e "/opt/scripts/tools" ]
then
	# expand partition to full disk
	cd /opt/scripts/tools
	sudo git pull
	sudo ./grow_partition.sh
fi
