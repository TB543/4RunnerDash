#!/bin/bash

# bluetooth
cd src
bluetoothctl power on
bluetoothctl discoverable-timeout 0
bluetoothctl discoverable on
bluetoothctl pairable on

# maps
../venv/bin/nominatim serve &
java -jar Lib/graphhopper.jar server ../resources/graphhopper_config.yml &
sudo docker stop tileserver
sudo docker rm tileserver
sudo docker run -d --name tileserver -v $(pwd)/Lib/tileserver:/data -v $(pwd)/AppData/map_data:/data/map_data -p 8080:8080 maptiler/tileserver-gl:latest
cd ..
