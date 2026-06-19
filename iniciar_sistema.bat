@echo off
cd /d "%~dp0"

start "Django" cmd /k "call .venv\Scripts\activate.bat && python manage.py runserver"
start "Scheduler" cmd /k "call .venv\Scripts\activate.bat && python manage.py run_scheduler"