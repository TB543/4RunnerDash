#!/bin/bash

# installs map database
mkdir -p ../src/AppData/map_data
wget -O ../src/AppData/map_data/map.osm.pbf https://download.geofabrik.de/north-america/us-latest.osm.pbf # only US, feel free to change to a different region if needed

# configures postgresql
sudo -u postgres /usr/lib/postgresql/15/bin/initdb -D ../src/AppData/map_data/postgresql
sudo systemctl restart postgresql
sudo -u postgres createuser -s $(whoami)
sudo -u postgres createuser www-data

# installs tilemaker
git clone https://github.com/systemed/tilemaker ../src/Lib/tilemaker
mkdir ../src/Lib/tilemaker/build
cd ../src/Lib/tilemaker/build
cmake ..
make -j$(nproc)
cd ..
./get-coastline.sh
./get-landcover.sh
cd ../../../resources

# creates swapfile for more memory
sudo fallocate -l 64G swapfile
sudo chmod 600 swapfile
sudo mkswap swapfile
sudo swapon swapfile

# configures map for nominatim
export NOMINATIM_FLATNODE_FILE=../src/AppData/map_data/flatnode.file
export NOMINATIM_IMPORT_STYLE=full
../venv/bin/nominatim import --osm-file ../src/AppData/map_data/map.osm.pbf --no-updates

# configures map for tilemaker and removes tilemaker
cd ../src/Lib/tilemaker
build/tilemaker --input ../../AppData/map_data/map.osm.pbf --output ../../AppData/map_data/map.mbtiles --config config.json --process process.lua --bbox -180,-90,180,90
cd ../../../resources
rm -rf ../src/Lib/tilemaker/

# configures map for graphhopper
cd ../src
java -Xmx64g -XX:InitiatingHeapOccupancyPercent=7 -jar Lib/graphhopper.jar import ../resources/graphhopper_config.yml
cd ../resources

# removes swapfile and shuts down system
sudo swapoff swapfile
rm -f swapfile
rmdir tokenizer
sudo shutdown
