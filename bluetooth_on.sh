#!/bin/bash

bluetoothctl power on
bluetoothctl discoverable-timeout 0
bluetoothctl discoverable on
bluetoothctl pairable on
