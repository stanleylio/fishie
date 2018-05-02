#!/bin/bash

cd
cd node
git pull

sudo apt update
sudo apt-get autoremove -y
sudo apt upgrade -y

cd ~/node/setup
bash backup_settings.sh
bash backup.sh
