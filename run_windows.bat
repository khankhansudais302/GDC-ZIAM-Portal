@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\activate.bat (
  echo First run setup_windows.bat and finish the setup.
  pause
  exit /b 1
)
call .venv\Scripts\activate
python manage.py runserver
pause
