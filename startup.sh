#!/bin/bash

# configures bluetooth settings
bluetoothctl power on
bluetoothctl discoverable-timeout 0
bluetoothctl discoverable on
bluetoothctl pairable on

# runs the program locally
cd src
~/4RunnerDash/venv/bin/python ~/4RunnerDash/src/AudioPlayback/BluezAgent.py &
sudo Xorg :0 | ~/4RunnerDash/venv/bin/python ~/4RunnerDash/src/main.py
cd .. 

# resets settings on exit
bluetoothctl power off
bluetoothctl discoverable off
bluetoothctl pairable off
pkill -f BluezAgent.py
