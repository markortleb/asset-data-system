#!/usr/bin/env bash

apt-get update
apt-get -y install sudo
sudo apt-get install -y wget
sudo apt-get install -y gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo 'deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse' | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-mongosh
sudo apt-get install -y cron
sudo apt-get install -y vim
service cron start
python -m pip install -r requirements.txt
