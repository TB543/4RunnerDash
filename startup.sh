#!/bin/bash

# runs the program
./start_backend.sh  # note: stop backend is called from within the python code on shutdown
cd src
sudo Xorg :0 | ../venv/bin/python main.py
cd ..
