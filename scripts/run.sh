#!/bin/sh
sudo source test_env_serv/venv-api/bin/activate
sudo cd server
sudo gunicorn server:app
