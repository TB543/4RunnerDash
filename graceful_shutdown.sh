#!/bin/bash

# maps
pkill -2 nominatim
pkill -f graphhopper
sudo docker stop tileserver
sudo docker rm tileserver

# bluetooth
bluetoothctl discoverable off
bluetoothctl pairable off
bluetoothctl power off

# waits for processes to exit and shuts down
while pgrep -f nominatim > /dev/null; do
    echo test
    sleep 1
done
while pgrep -f graphhopper > /dev/null; do
    sleep 1
done
while [ "$(sudo docker ps -q -f name=tileserver)" != "" ]; do
    echo "Waiting for Docker container to stop..."
    sleep 1
done
sudo shutdown
