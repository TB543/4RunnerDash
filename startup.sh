#!/bin/bash

# runs the program
./start_backend.sh  # note: stop backend is called from within the python code on shutdown
cd src
sudo Xorg :0 | ../venv/bin/python -u main.py 2>&1 | tee >(awk '/Starting Debug Logging/{flag=1; next} /Ending Debug Logging/{flag=0} flag' >> debug.log)
cd ..
