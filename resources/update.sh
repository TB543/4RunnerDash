#!/bin/bash

# pulls the latest release code from github
git checkout $(git describe --tags "$(git rev-list --tags --max-count=1)")

# runs update scripts
cd patches/
/bin/bash ./update.sh
cd ..

# removes update scripts and reboots
rm -rf patches/
sudo reboot
