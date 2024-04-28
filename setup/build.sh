#!/bin/bash
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
python3 manage.py collectstatic

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell < setup/adminuser.py