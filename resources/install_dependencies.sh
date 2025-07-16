#!/bin/bash

# installs dependencies
sudo apt install -y xserver-xorg x11-xserver-utils fonts-noto-color-emoji # display 
sudo apt install -y python3.11-dev python3-tk python3-gi # python src dependencies
sudo apt install -y bluez pulseaudio pulseaudio-module-bluetooth # bluetooth/audio system
sudo apt install -y openjdk-17-jdk postgresql postgis osm2pgsql libicu-dev # navigation system

# installs python modules
python3 -m venv ../venv --system-site-packages
../venv/bin/pip install -r requirements.txt

# installs graphhopper (used for gps directions)
mkdir ../src/Lib
wget -O ../src/Lib/graphhopper.jar https://github.com/graphhopper/graphhopper/releases/download/10.2/graphhopper-web-10.2.jar

# installs map database
mkdir -p ../src/AppData/map_data
wget -O ../src/AppData/map_data/map.osm.pbf https://download.geofabrik.de/north-america/us-latest.osm.pbf # only US, feel free to change to a different region if needed

# creates swapfile for more memory
sudo fallocate -l 64G swapfile
sudo chmod 600 swapfile
sudo mkswap swapfile
sudo swapon swapfile

# configures map for graphhopper
cd ../src
java -Xmx64g -XX:InitiatingHeapOccupancyPercent=7 -jar Lib/graphhopper.jar import ../resources/graphhopper_config.yml
cd ../resources

# configures map for nominatim
sudo -u postgres createuser -s $(whoami)
sudo -u postgres createuser www-data
export NOMINATIM_FLATNODE_FILE=../src/AppData/map_data/flatnode.file
export NOMINATIM_IMPORT_STYLE=full
../venv/bin/nominatim import --osm-file ../src/AppData/map_data/map.osm.pbf --no-updates 

# removes swapfile and shuts down system
sudo swapoff swapfile
rm -f swapfile
sudo shutdown
