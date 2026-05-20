@echo off
title Build Autonomous AI Commerce Final MVP EXE
color 0A

cd /d C:\Users\omen\AutonomousAICommerce

call venv\Scripts\activate

pip install -r requirements.txt

pyinstaller --noconfirm --onedir ^
--name AutonomousAICommerce ^
--add-data "app;app" ^
--add-data "static;static" ^
--hidden-import fastapi ^
--hidden-import fastapi.staticfiles ^
--hidden-import fastapi.responses ^
--hidden-import uvicorn ^
--hidden-import starlette ^
--hidden-import pydantic ^
--hidden-import pydantic_settings ^
--hidden-import httpx ^
--hidden-import sqlalchemy ^
--hidden-import apscheduler ^
--hidden-import dotenv ^
--hidden-import jinja2 ^
run_server.py

xcopy /E /I /Y static dist\AutonomousAICommerce\static

echo.
echo Final MVP build complete.
echo Run:
echo C:\Users\omen\AutonomousAICommerce\dist\AutonomousAICommerce\AutonomousAICommerce.exe
pause
