Remove-Item ./venv -Recurse
Remove-Item ./static/* -Recurse

python -m venv ./venv
./venv/Scripts/activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic

./setup/config_db.ps1