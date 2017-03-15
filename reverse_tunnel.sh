#!/bin/bash
#https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html

# sudo apt install autossh
# create user for this node on the remote host
#sudo useradd -m kmet-bbb3
#sudo passwd kmet-bbb3
#sudo chsh -s /bin/bash kmet-bbb3
# do the ssh-copy-id dance

RemotePort=10024

# glazerlab-i7nuc
RemoteHost=128.171.153.115
# otg-met
#Host=166.122.96.11
# kmet-rpi1
#Host=166.122.96.119

autossh -M 19922 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$RemoteHost -p 22
