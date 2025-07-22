#!/bin/bash

# runs the program
cd src
../start_backend.sh
sudo Xorg :0 | ~/4RunnerDash/venv/bin/python ~/4RunnerDash/src/main.py
cd ..
