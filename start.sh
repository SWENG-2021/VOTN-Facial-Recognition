sudo apt-get update
sudo apt install ffmpeg 
sudo apt-get install python3-pip python3-dev nginx
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-available/default
sudo touch /etc/nginx/sites-available/votn.com
sudo chown -R $USER:$USER /etc/nginx/sites-available/votn.com
sudo cat server_config > /etc/nginx/sites-available/votn.com
sudo sed -i 's/_serv1_/www.votn.com/' /etc/nginx/sites-available/votn.com
sudo sed -i 's/_serv2_/votn.com/' /etc/nginx/sites-available/votn.com
sudo ln -f -s /etc/nginx/sites-available/votn.com /etc/nginx/sites-enabled/votn.com
sudo service nginx restart
sudo pip3 install virtualenv
sudo virtualenv venv-api
source venv-api/bin/activate
sudo pip3 install -r requirements.txt
sudo pip3 install gunicorn
sudo gunicorn server:app

