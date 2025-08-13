#!/bin/bash

# runs the program
./start_backend.sh
cd src
sudo Xorg :0 | ../venv/bin/python main.py
cd ..
./stop_backend.sh
