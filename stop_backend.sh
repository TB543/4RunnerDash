#!/bin/bash

# save system time to CarPiHat
sudo hwclock -w -f /dev/rtc1

# maps
pkill -2 nominatim
pkill -f graphhopper
sudo docker stop tileserver
sudo docker rm tileserver

# bluetooth
bluetoothctl discoverable off
bluetoothctl pairable off
bluetoothctl power off

# waits for processes to exit
while pgrep -f nominatim > /dev/null; do
    sleep 1
done
while pgrep -f graphhopper > /dev/null; do
    sleep 1
done
while [ "$(sudo docker ps -q -f name=tileserver)" != "" ]; do
    sleep 1
done
