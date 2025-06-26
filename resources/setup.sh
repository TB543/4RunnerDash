#!/bin/bash

# installs and configures the display for startup
sudo apt update
sudo apt install -y xserver-xorg
sudo cp boot-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable boot-display.service

# creates venv and installs dependencies
python3 -m venv ../venv
sudo apt install -y python3-tk
../venv/bin/pip install -r requirements.txt

# sets up src to run on boot and reboots the system
cat boot-commands.txt >> ~/.bashrc
sudo reboot
