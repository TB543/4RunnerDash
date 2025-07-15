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
sudo fallocate -l 64G swapfile
sudo chmod 600 swapfile
sudo mkswap swapfile
sudo swapon swapfile

# installs and configures map database
mkdir -p ../src/AppData/map_data
wget -O ../src/AppData/map_data/map.osm.pbf https://download.geofabrik.de/north-america/us-latest.osm.pbf # only US, feel free to change to a different region if needed
osrm-extract -p OSRM_profile/car.lua ../src/AppData/map_data/map.osm.pbf 2>&1 | tee osrm-extract.log  # 2>&1 | tee osrm-extract.log only for debugging
osrm-partition ../src/AppData/map_data/map.osrm 2>&1 | tee osrm-partition.log  # 2>&1 | tee osrm-partition.log only for debugging
osrm-customize ../src/AppData/map_data/map.osrm 2>&1 | tee osrm-customize.log  # 2>&1 | tee osrm-customize.log only for debugging

# installs Nominatim (used to get gps coordinates from address)
wget https://www.nominatim.org/release/Nominatim-5.1.0.tar.bz2
tar xvf Nominatim-5.1.0.tar.bz2 -C ..
rm Nominatim-5.1.0.tar.bz2
../venv/bin/pip install ../Nominatim-5.1.0/packaging/nominatim-{api,db}
rm -rf ../Nominatim-5.1.0
sudo -u postgres createuser -s $(whoami)
sudo -u postgres createuser www-data
export NOMINATIM_FLATNODE_FILE=../src/AppData/map_data/flatnode.file
export NOMINATIM_IMPORT_STYLE=full
../venv/bin/nominatim import --osm-file ../src/AppData/map_data/map.osm.pbf --no-updates 2>&1 | tee nominatim.log  # 2>&1 | tee nominatim.log only for debugging

# removes swapfile and shuts down system
sudo swapoff swapfile
rm -f swapfile
sudo shutdown
