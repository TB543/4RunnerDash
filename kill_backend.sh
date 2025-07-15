#!/bin/bash

# bluetooth
bluetoothctl power off
bluetoothctl discoverable off
bluetoothctl pairable off

# maps
sudo killall java
