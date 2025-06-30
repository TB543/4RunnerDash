# sets the display and touch screen variables
if [[ -n "$SSH_CLIENT" ]]; then
    export DISPLAY=$(echo $SSH_CLIENT | awk '{print $1}'):0.0
else
    export DISPLAY=:0
fi
