#!/bin/bash

# runs the program
./start_backend.sh
cd src
sudo Xorg :0 | ../venv/bin/python -u main.py 2>&1 | tee >(awk '/Starting Debug Logging/{flag=1; next} /Ending Debug Logging/{flag=0} flag' >> debug.log)
PY_EXIT_CODE="${PIPESTATUS[1]}"
cd ..
./stop_backend.sh

# processes return code of program
if [ "$PY_EXIT_CODE" -eq 201 ]; then  # update
    ./resources/update.sh
fi
if [ "$PY_EXIT_CODE" -ne 200 ]; then  # 200 is exit code for do nothing, anything else shuts down to preserve battery life
    sudo shutdown now
fi
