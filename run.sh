#!/bin/bash
source .env/bin/activate
export FLASK_APP=pid_flask.py
echo "*******************8"
echo "Open you browser at http://localhost:5000"
flask run
