#!/bin/bash

# ensures drive mount permission
sudo chown -R $USER:$USER src/AppData/map_data
chmod -R u+rwX src/AppData/map_data

# runs the program
cd src
../start_backend.sh
sudo Xorg :0 | ~/4RunnerDash/venv/bin/python ~/4RunnerDash/src/main.py
cd ..
