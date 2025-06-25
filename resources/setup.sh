# installs and configures the display for startup
sudo apt install xserver-xorg
sudo mv boot-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable boot-display.service

# creates venv and installs dependencies
python3 -m venv ../venv
sudo apt install python3-tk
source ../venv/bin/activate
pip install -r requirements.txt

# sets up src to run on boot and reboots the system
cat boot-commands.txt >> ~/.bashrc
sudo reboot
