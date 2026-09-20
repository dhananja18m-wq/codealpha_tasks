@echo off
title ShopEase - Starting Server
echo ==================================================
echo           SHOPEASE - E-COMMERCE STORE
echo ==================================================
echo.
echo [1/2] Running database migrations...
python manage.py migrate

echo.
echo [2/2] Opening ShopEase in your browser...
start http://127.0.0.1:8000/

echo.
echo Starting Django Development Server on http://127.0.0.1:8000/
echo Press Ctrl+C in this window to stop the server.
echo ==================================================
echo.

python manage.py runserver 8000
pause
