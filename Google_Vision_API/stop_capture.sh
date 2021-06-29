#!/bin/bash

echo "Hello From Stop Capture"
sleep 2
sudo pkill guvcview
sleep 1
python3 /home/pi/TestGoogleAPI.py

exit 0