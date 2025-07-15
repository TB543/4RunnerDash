#!/bin/bash

./mount_permission.sh
./bluetooth_on.sh
cd src
sudo Xorg :0 | ~/4RunnerDash/venv/bin/python ~/4RunnerDash/src/main.py
cd ..
#./bluetooth_off.sh
