#!/bin/bash

# installs and configures the display for startup
sudo apt install -y xserver-xorg
sudo apt install -y x11-xserver-utils
sudo cp boot-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable boot-display.service

# creates venv and installs dependencies
python3 -m venv ../venv
sudo apt install -y python3.11-dev
sudo apt install -y python3-tk
sudo apt install -y fonts-noto-color-emoji
../venv/bin/pip install -r requirements.txt

# sets up src to run on boot and reboots the system
cat boot-commands.txt >> ~/.bashrc
sudo apt update
sudo reboot
