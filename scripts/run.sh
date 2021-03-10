#!/bin/sh
sudo apt install python3 -y
sudo apt install python3-pip -y
pip3 install flask
sudo apt-get install nginx
sudo apt-get install gunicorn3
python3 server/server.py
