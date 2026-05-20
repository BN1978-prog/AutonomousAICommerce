@echo off
title Build Autonomous AI Commerce EXE
color 0A
cd /d %~dp0

if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller pydantic-settings

if not exist run_server.py (
    echo run_server.py missing
    pause
    exit /b 1
)

pyinstaller --noconfirm --onedir ^
--name AutonomousAICommerce ^
--add-data "app;app" ^
--add-data "static;static" ^
--hidden-import fastapi ^
--hidden-import fastapi.staticfiles ^
--hidden-import fastapi.responses ^
--hidden-import uvicorn ^
--hidden-import uvicorn.logging ^
--hidden-import uvicorn.loops ^
--hidden-import uvicorn.loops.auto ^
--hidden-import uvicorn.protocols ^
--hidden-import uvicorn.protocols.http ^
--hidden-import uvicorn.protocols.http.auto ^
--hidden-import starlette ^
--hidden-import starlette.staticfiles ^
--hidden-import starlette.responses ^
--hidden-import pydantic ^
--hidden-import pydantic_settings ^
run_server.py

echo.
echo Build finished.
echo Run: dist\AutonomousAICommerce\AutonomousAICommerce.exe
echo.
pause
