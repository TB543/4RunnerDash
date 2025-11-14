#!/bin/bash

# ensures a version is given
if [ -z "$1" ]; then
    echo "usage: $0 <tag_name>"
    exit 1
fi

# pulls the latest release code from github
git fetch --tags
git checkout $1

# runs update scripts
cd patches/
/bin/bash ./update.sh
cd ..

# removes update scripts and reboots
rm -rf patches/
sudo reboot
