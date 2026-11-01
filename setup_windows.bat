@echo off
setlocal
cd /d "%~dp0"
echo ========================================
echo GDC ZIAM Secure Portal - Setup
echo ========================================
py -m venv .venv
if errorlevel 1 goto error
call .venv\Scripts\activate
if errorlevel 1 goto error
python -m pip install -r requirements.txt
if errorlevel 1 goto error
python manage.py makemigrations portal
if errorlevel 1 goto error
python manage.py migrate
if errorlevel 1 goto error
echo.
echo Now create the first Principal/Admin account.
python manage.py createsuperuser
if errorlevel 1 goto error
echo.
echo Setup complete. Run run_windows.bat to start the local website.
pause
exit /b 0
:error
echo Setup stopped because a command failed. Read the error above.
pause
exit /b 1
