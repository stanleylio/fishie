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
map[base-009]=10029
map[base-010]=10030
map[base-011]=10031
map[base-012]=10032
map[base-013]=10033
map[base-014]=10034
map[base-015]=10035
map[base-016]=10036
map[base-017]=10037
map[base-018]=10038
map[base-019]=10039
map[base-020]=10040
map[base-021]=10041
map[base-022]=10042
map[base-023]=10043
map[base-024]=10044
map[base-025]=10045
map[base-026]=10046
map[base-027]=10047
map[base-028]=10048

map[node-080]=10180
map[node-084]=10184
map[node-085]=10185
map[node-086]=10186
map[node-112]=10212
map[node-113]=10213
map[node-114]=10214


RemotePort=${map[$(hostname)]}

# UHM
RemoteHost=grog.soest.hawaii.edu
# otg-met
#Host=166.122.96.11
# kmet-rpi1
#Host=166.122.96.119

# debug
#autossh -M 19922 -N -vv -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$RemoteHost -p 22
autossh -M 19922 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$RemoteHost -p 22
autossh -M 19924 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$RemoteHost -p 2222
