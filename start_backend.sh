#!/bin/bash

# stops old backend
./stop_backend.sh
cd src

# bluetooth
bluetoothctl power on
bluetoothctl discoverable-timeout 0
bluetoothctl discoverable on
bluetoothctl pairable on

# maps
nohup ../venv/bin/nominatim serve > /dev/null 2>&1 &
nohup java -jar Lib/graphhopper.jar server ../resources/graphhopper_config.yml > /dev/null 2>&1 &
sudo docker run -d --name tileserver -v $(pwd)/Lib/tileserver:/data -v $(pwd)/AppData/map_data:/data/map_data -p 8080:8080 maptiler/tileserver-gl:latest
cd ..
