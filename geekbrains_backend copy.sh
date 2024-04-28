#!/bin/bash

source venv/bin/activate
exec uvicorn geekbrains_backend.asgi:application --host 127.0.0.1 --port 8000 --workers 5