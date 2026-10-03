#!/bin/bash

# save system time to CarPiHat
sudo hwclock -w -f /dev/rtc1

# bluetooth
bluetoothctl discoverable off
bluetoothctl pairable off
bluetoothctl power off

# waits for processes to exit
while pgrep -f nominatim > /dev/null; do
    pkill -9 -f nominatim
    sleep 1
done
while pgrep -f graphhopper > /dev/null; do
    pkill -9 -f graphhopper
    sleep 1
done
while [ "$(sudo docker ps -q -f name=tileserver)" != "" ]; do
    sudo docker stop tileserver
    sudo docker rm tileserver
    sleep 1
done
