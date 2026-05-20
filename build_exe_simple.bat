@echo off
title Build Autonomous AI Commerce EXE
color 0A

echo ========================================
echo Building Autonomous AI Commerce EXE
echo ========================================

cd /d C:\Users\omen\AutonomousAICommerce

if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Searching entry point...

if exist app\main.py (
    set ENTRY=app\main.py
) else (
    echo app\main.py not found.
    echo Checking possible files...
    dir app
    pause
    exit /b
)

echo.
echo Building EXE from %ENTRY%...

pyinstaller ^
--noconfirm ^
--onefile ^
--name AutonomousAICommerce ^
%ENTRY%

echo.
echo ========================================
echo BUILD FINISHED
echo ========================================
echo.

echo Check this folder:
echo C:\Users\omen\AutonomousAICommerce\dist

pause