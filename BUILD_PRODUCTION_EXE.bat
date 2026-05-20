@echo off
title Build Autonomous AI Commerce Production EXE
color 0A

cd /d C:\Users\omen\AutonomousAICommerce

call venv\Scripts\activate

pip install -r requirements.txt

pyinstaller --noconfirm --onedir ^
--name AutonomousAICommerce ^
--add-data "app;app" ^
--add-data "static;static" ^
--add-data ".env;.env" ^
--hidden-import fastapi ^
--hidden-import fastapi.staticfiles ^
--hidden-import fastapi.responses ^
--hidden-import uvicorn ^
--hidden-import starlette ^
--hidden-import pydantic ^
--hidden-import pydantic_settings ^
--hidden-import httpx ^
--hidden-import sqlalchemy ^
--hidden-import psycopg2 ^
--hidden-import psycopg2_binary ^
--hidden-import dotenv ^
--hidden-import structlog ^
--hidden-import pythonjsonlogger ^
--hidden-import pythonjsonlogger ^
--hidden-import pythonjsonlogger.jsonlogger ^
run_server.py

xcopy /E /I /Y static dist\AutonomousAICommerce\static

echo.
echo Production build complete.
echo Run Start_Production.bat
pause
