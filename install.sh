#!/bin/bash
sudo apt-get update
sudo apt install ffmpeg 
sudo apt-get install python3-pip python3-dev nginx
sudo pip3 install cmake -vvv
sudo pip3 install face_recognition -vvv
sudo pip3 install scikit-build -vvv
sudo pip3 install opencv-python -vvv
sudo pip3 install gunicorn -vvv
sudo pip3 install -Iv frameioclient==0.9.1 -vvv
sudo pip3 install flask -vvv
