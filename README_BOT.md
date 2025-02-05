# questions_sentement_bot
***
## DOCKER
К сожалению, нам не хватило времени создать docker контейнер, однако, даже без этого, запустить проект, не составит большого труда.
***
## Версия Python
Python 3.10 и выше
***
## Как запустить
1. Скачать модель с [гугл диска](https://drive.google.com/file/d/1NmGcfx5W4TXtQkVs4wAcMpP5qpiKwan4/view?usp=drive_link) и вставить в папку [src/](src/)
2. Установить зависимости
* Powersheell
>```powershell
>./setup/build.ps1
>```
* Bash
>```bash
>source setup/build.sh
>```
3. Запусть Django
>```powershell
>./venv/Scripts/activate
>uvicorn geekbrains_backend.asgi:application --host 127.0.0.1 --port 8000 --reload --log-level info
>```
* Bash
>```bash
>source geekbrains_backend.sh
>```
5. Запусть Telegram bot
>```powershell
>./venv/Scripts/activate
>python ./bot/main2.py
>```
* Bash
>```bash
>source geekbrains_bot.sh
>```
***
## Админ-панель Django
админка доступна по пути http://127.0.0.1/admin
логин: superuser
пароль: superuser
***
##  Бот телеграм
https://t.me/digital_break_test_bot
