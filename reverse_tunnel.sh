#!/bin/bash
#https://raymii.org/s/tutorials/Autossh_persistent_tunnels.html

# of course, sudo apt install autossh and do the ssh-copy-id dance from the remote host first.

Host=128.171.153.115
#Host=166.122.97.82
RemotePort=10032

autossh -M 19922 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R $RemotePort:localhost:22 $(hostname)@$Host -p 22
#autossh -M 19922 -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -R 10032:localhost:22 kmet-bbb2@166.122.97.82 -p 22
