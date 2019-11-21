#!/bin/bash
source .env/bin/activate
export FLASK_APP=pid_flask.py
flask run
