#!/bin/bash

# runs the program
./start_backend.sh
cd src
sudo Xorg :0 | ../venv/bin/python -u main.py 2>&1 | tee >(awk '/Starting Debug Logging/{flag=1; next} /Ending Debug Logging/{flag=0} flag' >> debug.log)
PY_EXIT_CODE="${PIPESTATUS[1]}"
cd ..
./stop_backend.sh

# processes return code of program
if [ "$PY_EXIT_CODE" -eq 200 ]; then  # shutdown
    sudo shutdown now
elif [ "$PY_EXIT_CODE" -eq 201 ]; then  # update
    ./resources/update.sh
fi
