#!/bin/bash

set -e
set -x

echo "Provisioning starts!"

#sudo -s
sudo apt-get update
sudo apt-get install -y python-pip  python-dev imagemagick libmagickwand-dev lynx
# apt-get install -y nginx
sudo pip install --upgrade pip

sudo pip install -r requirements.txt

#Config Gunicorn:
sudo cp ./color_count.service /etc/systemd/system/ #ln -s will not work
sudo systemctl start color_count.service
sudo systemctl enable color_count.service

FLASK_APP=color_count.py flask initdb

echo "Provisioning complete!"
