#!/bin/bash

# runs the program
./start_backend.sh
cd src
sudo Xorg :0 | ~/4RunnerDash/venv/bin/python ~/4RunnerDash/src/main.py
cd ..
