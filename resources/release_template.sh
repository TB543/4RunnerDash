#!/bin/bash

# ensures a version is given
if [ -z "$1" ]; then
    echo "usage: $0 <tag_name>"
    exit 1
fi

# pulls the latest release code from github
cd ..
git fetch --tags
git checkout $1

# ======================== ADD ADDITIONAL INSTALL COMMANDS HERE ========================

# ======================== ADD ADDITIONAL INSTALL COMMANDS HERE ========================

# removes update scripts and reboots
rm -rf $1
sudo reboot