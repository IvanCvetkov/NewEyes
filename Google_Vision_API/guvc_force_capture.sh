#!/bin/bash

echo "Hello From Start Capture"

guvcview -i /home/pi/Desktop/output.jpg -g none -p /home/pi/default.gpfl -n 1 -t 2

exit 0