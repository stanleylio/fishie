#!/bin/bash

cd
cd node
git pull

sudo apt update
sudo apt autoremove
sudo apt upgrade -y

cd ~/node/setup
bash backup_settings.sh
bash backup.sh
