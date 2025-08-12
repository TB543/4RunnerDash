#!/bin/bash

# sets up the boot commands
sudo cp startup@.service /etc/systemd/user/
systemctl --user daemon-reload
systemctl --user enable startup@$(whoami).service

# configures PiCarHAT DAC
sudo sed -i 's/^dtparam=audio=on/#dtparam=audio=on/' /boot/firmware/config.txt
echo -e "\ndtoverlay=hifiberry-dacplus-std\ndtoverlay=vc4-kms-v3d,noaudio" | sudo tee -a /boot/firmware/config.txt

# gets environment variables
clear
grep -i "N: Name=" /proc/bus/input/devices
read -p "Above is a list of connected devices, copy and paste the one for the touch screen (just the text in the quotes): " TOUCH_SCREEN
read -p "Enter your Spotify API client ID: " CLIENT_ID
read -p "Enter your Spotify API client secret: " CLIENT_SECRET
cat env.sh >> ~/.bashrc
sudo sed -i "/^\[Service\]/a Environment=TOUCH_SCREEN=\"$TOUCH_SCREEN\"\nEnvironment=CLIENT_ID=\"$CLIENT_ID\"\nEnvironment=CLIENT_SECRET=\"$CLIENT_SECRET\"" /etc/systemd/user/startup@.service
echo -e "export TOUCH_SCREEN='$TOUCH_SCREEN'\nexport CLIENT_ID='$CLIENT_ID'\nexport CLIENT_SECRET='$CLIENT_SECRET'" >> ~/.bashrc
