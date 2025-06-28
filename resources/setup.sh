#!/bin/bash

# installs dependencies
sudo apt install -y xserver-xorg x11-xserver-utils python3.11-dev python3-tk python3-gi fonts-noto-color-emoji bluez
python3 -m venv ../venv --system-site-packages
../venv/bin/pip install -r requirements.txt

# sets up the boot commands
sudo cp boot-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable boot-display.service
cat boot-commands.txt >> ~/.bashrc
sudo reboot
