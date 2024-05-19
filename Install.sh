#!/bin/bash

cd ~
sudo apt-get install libpng12-dev -y
sudo apt-get install python-pkg-resources python3-pkg-resources -y
sudo git clone https://github.com/HoolyHoo/PiSugarbatterymonitor.git
sudo chmod 755 /home/pi/PiSugarbatterymonitor/HHMonitorStart.sh
sudo chmod 755 /home/pi/PiSugarbatterymonitor/Pngview/pngview
