#!/bin/bash
set -e
set -x

echo "Provisioning Reverse Proxy on EC2!"

apt-get update
apt-get install -y nginx lynx 

#cd ~
#git clone https://github.com/mw866/one-and-done.git

#Config NGINX:
ln -s  "$(pwd)/color_count" /etc/nginx/sites-available/
ln -s "$(pwd)/color_count" /etc/nginx/sites-enabled/
sudo rm -rf /etc/nginx/sites-enabled/default
systemctl restart nginx


echo "Provisioning complete!"
