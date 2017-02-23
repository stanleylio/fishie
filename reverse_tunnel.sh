#!/bin/bash
#https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html

# sudo apt install autossh
# create user for this node on the remote host
#sudo useradd -m kmet-bbb3
#sudo passwd kmet-bbb3
#sudo chsh -s /bin/bash kmet-bbb3
# do the ssh-copy-id dance

RemotePort=10033

# glazerlab-i7nuc
Host=128.171.153.115
autossh -M 19922 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$Host -p 22

# otg-met
#Host=166.122.96.11
#autossh -M 19923 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$Host -p 22

# kmet-rpi1
#Host=166.122.96.119
#autossh -M 19924 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$Host -p 22
