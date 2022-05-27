#!/bin/bash

echo "Synchronize time..."
sudo /etc/init.d/ntp stop
sudo ntpd -q -g
sudo /etc/init.d/ntp start

exit 0
