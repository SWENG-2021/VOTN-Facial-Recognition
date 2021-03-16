#!/bin/sh
source test_env_serv/venv-api/bin/activate
cd server
gunicorn server:app
