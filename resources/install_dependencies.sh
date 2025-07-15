#!/bin/bash

# installs dependencies
sudo apt install -y xserver-xorg x11-xserver-utils # display 
sudo apt install -y python3.11-dev python3-tk python3-gi fonts-noto-color-emoji # python modules and emoji rendering
sudo apt install -y bluez pulseaudio pulseaudio-module-bluetooth # bluetooth/audio system
sudo apt install -y build-essential git cmake pkg-config libbz2-dev libxml2-dev libzip-dev libboost-all-dev lua5.2 liblua5.2-dev libtbb-dev # OSRM dependencies 
sudo apt install -y postgresql postgis osm2pgsql # Nominatim dependencies

# installs python modules
python3 -m venv ../venv --system-site-packages
../venv/bin/pip install -r requirements.txt

# installs and builds OSRM (used for gps directions)
git clone --branch v6.0.0 https://github.com/Project-OSRM/osrm-backend.git ../OSRM
mkdir ../OSRM/build
cd ../OSRM/build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-Wno-array-bounds -Wno-uninitialized -include utility"
cmake --build .
sudo cmake --build . --target install
cd ../../resources/
rm -rf ../OSRM/

# creates swapfile for more memory
sudo fallocate -l 12G swapfile
sudo chmod 600 swapfile
sudo mkswap swapfile
sudo swapon swapfile

# installs and configures map database
wget -O ../src/AppData/map.osm.pbf https://download.geofabrik.de/north-america/us-latest.osm.pbf # only US, feel free to change to a different region if needed
osrm-extract -p OSRM_profile/car.lua ../src/AppData/map.osm.pbf
osrm-partition ../src/AppData/map.osrm
osrm-customize ../src/AppData/map.osrm

# installs Nominatim (used to get gps coordinates from address)
wget https://www.nominatim.org/release/Nominatim-5.1.0.tar.bz2
tar xvf Nominatim-5.1.0.tar.bz2 -C ..
rm Nominatim-5.1.0.tar.bz2
../venv/bin/pip install ../Nominatim-5.1.0/packaging/nominatim-{api,db}
rm -rf ../Nominatim-5.1.0
cd ../src
sudo -u postgres createuser -s $(whoami)
sudo -u postgres createuser www-data
../venv/bin/nominatim import --osm-file ../src/AppData/map.osm.pbf
cd ../resources
../venv/bin/pip install uvicorn falcon

# removes swapfile and restarts system
sudo swapoff swapfile
rm -f swapfile
sudo shutdown
