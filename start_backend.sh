#!/bin/bash

# bluetooth
bluetoothctl power on
bluetoothctl discoverable-timeout 0
bluetoothctl discoverable on
bluetoothctl pairable on

# maps
java -jar Lib/graphhopper.jar server ../resources/graphhopper_config.yml &
