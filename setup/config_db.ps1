Remove-Item */migrations/*  -Exclude __init__.py -Recurse
Remove-Item ./db.sqlite3

python manage.py makemigrations
python manage.py migrate

Get-Content ./setup/adminuser.py | python manage.py shell