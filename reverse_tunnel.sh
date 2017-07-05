#!/bin/bash
#https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html

# sudo apt install autossh
# create user for this node on the remote host
#sudo useradd -m kmet-bbb3
#sudo passwd kmet-bbb3
#sudo chsh -s /bin/bash kmet-bbb3
# do the ssh-copy-id dance

declare -A map
map[base-001]=10021
map[base-002]=10022
map[base-003]=10023
map[base-004]=10024
map[base-005]=10025
map[base-006]=10026
map[base-007]=10027
map[base-008]=10028
map[kmet-rpi1]=10034

RemotePort=${map[$(hostname)]}

# glazerlab-i7nuc
RemoteHost=128.171.153.115
# otg-met
#Host=166.122.96.11
# kmet-rpi1
#Host=166.122.96.119

# debug
#autossh -M 19922 -N -vv -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$RemoteHost -p 22
autossh -M 19922 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$RemoteHost -p 22
