#!/bin/bash
#https://juliansimioni.com/blog/howto-access-a-linux-machine-behind-a-home-router-with-ssh-tunnels/

HostA=128.171.153.115

createTunnel() {
    /usr/bin/ssh -f -N -R 10023:localhost:22 -L19922:$HostA:22 $HostA
    if [[ $? -eq 0 ]]; then
        echo Tunnel to $HostA created successfully
    else
        echo An error occurred creating a tunnel to $HostA. Return code: $?
    fi
}
/usr/bin/ssh -p 19922 localhost ls > /dev/null
if [[ $? -ne 0 ]]; then
    echo Creating new tunnel connection to $HostA
    createTunnel
fi
