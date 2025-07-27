#!/bin/bash

# installs dependencies
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh # rust - needed for text to speech python module
sudo apt install -y xserver-xorg x11-xserver-utils fonts-noto-color-emoji # display 
sudo apt install -y python3.11-dev python3-tk python3-gi python3-mapnik gir1.2-gstreamer-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good # python src dependencies
sudo apt install -y bluez pulseaudio pulseaudio-module-bluetooth # bluetooth/audio system
sudo apt install -y cmake libboost-all-dev libshp-dev rapidjson-dev liblua5.3-dev libsqlite3-dev # tilemaker
sudo apt install -y openjdk-17-jdk postgresql postgis osm2pgsql libicu-dev acl docker.io # navigation system

# moves postgresql database to correct location
DIR=$(realpath ../src/AppData/map_data/postgresql)
while [ "$DIR" != "/" ]; do
    sudo setfacl -m u:postgres:x "$DIR"
    DIR=$(dirname "$DIR")
done
mkdir -p ../src/AppData/map_data/postgresql
sudo chown -R postgres:postgres ../src/AppData/map_data/postgresql
sudo sed -i.bak "s|^data_directory *=.*|data_directory = '$(realpath ../src/AppData/map_data/postgresql)'|" /etc/postgresql/15/main/postgresql.conf

# adds rust to shell and installs python modules
. "$HOME/.cargo/env"
python3 -m venv ../venv --system-site-packages
../venv/bin/pip install -r requirements.txt

# installs graphhopper (used for gps directions)
wget -O ../src/Lib/graphhopper.jar https://github.com/graphhopper/graphhopper/releases/download/10.2/graphhopper-web-10.2.jar

# installs tileserver and config files
sudo systemctl enable --now docker
sudo docker pull maptiler/tileserver-gl:latest
wget https://github.com/maptiler/tileserver-gl/releases/download/v1.3.0/test_data.zip
unzip test_data.zip -d ../src/Lib/tileserver
rm test_data.zip
sed -i 's#"mbtiles": "zurich_switzerland.mbtiles"#"mbtiles": "map_data/map.mbtiles"#' ../src/Lib/tileserver/config.json
