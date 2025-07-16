#!/bin/bash

# formats drive
clear
lsblk
read -p "Above is a list of connected devices, copy and paste the one for the drive (just the text after the "└─" character): " DRIVE

# mounts drive and makes mount persist over reboots
sudo mkfs.ext4 /dev/"$DRIVE"
mkdir -p ../src/AppData/map_data
sudo mount /dev/"$DRIVE" ../src/AppData/map_data
echo "/dev/$DRIVE  $(realpath ../src/AppData/map_data)  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload

# ensures drive has correct permissions
sudo chown -R $USER:$USER ../src/AppData/map_data
chmod -R u+rwX ../src/AppData/map_data
