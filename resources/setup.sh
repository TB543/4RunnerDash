#!/bin/bash

# installs dependencies
sudo apt install -y xserver-xorg x11-xserver-utils python3.11-dev python3-tk python3-gi fonts-noto-color-emoji bluez pulseaudio pulseaudio-module-bluetooth
python3 -m venv ../venv --system-site-packages
../venv/bin/pip install -r requirements.txt

# sets up the boot commands
sudo cp boot-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable boot-display.service

# asks user for the name of the display
clear
grep -i "N: Name=" /proc/bus/input/devices
read -p "Above is a list of connected devices, copy and paste the one for the touch screen (just the text in the quotes): " TOUCH_SCREEN
echo "export TOUCH_SCREEN='$TOUCH_SCREEN'" >> ~/.bashrc
cat boot-commands.txt >> ~/.bashrc
sudo reboot
