@echo off
title Autonomous AI Commerce System Builder
color 0A

echo ========================================
echo Autonomous AI Commerce System
echo Windows EXE Builder
echo ========================================

REM ----------------------------------------
REM CHECK PYTHON
REM ----------------------------------------

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
echo.
echo Python not found.
echo Install Python 3.11+
pause
exit /b
)

REM ----------------------------------------
REM CHECK NODE
REM ----------------------------------------

node --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
echo.
echo Node.js not found.
echo Install Node.js 20+
pause
exit /b
)

REM ----------------------------------------
REM CHECK RUST
REM ----------------------------------------

rustc --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
echo.
echo Rust not found.
echo Install Rust from:
echo https://rustup.rs
pause
exit /b
)

REM ----------------------------------------
REM CREATE VENV
REM ----------------------------------------

if not exist venv (
echo.
echo Creating virtual environment...
python -m venv venv
)

call venv\Scripts\activate

REM ----------------------------------------
REM INSTALL PYTHON DEPENDENCIES
REM ----------------------------------------

echo.
echo Installing Python dependencies...

pip install --upgrade pip

pip install ^
fastapi ^
uvicorn ^
sqlalchemy ^
pydantic ^
requests ^
aiohttp ^
openai ^
anthropic ^
pytest ^
pyinstaller

REM ----------------------------------------
REM BUILD BACKEND EXE
REM ----------------------------------------

echo.
echo Building backend executable...

pyinstaller ^
--noconfirm ^
--onefile ^
--name AutonomousAIBackend ^
backend\main.py

REM ----------------------------------------
REM CHECK DESKTOP FOLDER
REM ----------------------------------------

if not exist desktop (
echo.
echo Desktop folder not found.
echo Skipping Tauri build.
goto END
)

REM ----------------------------------------
REM INSTALL FRONTEND DEPENDENCIES
REM ----------------------------------------

echo.
echo Installing frontend dependencies...

cd desktop

call npm install

REM ----------------------------------------
REM BUILD TAURI APP
REM ----------------------------------------

echo.
echo Building desktop application...

call npm run tauri build

cd ..

REM ----------------------------------------
REM CREATE RELEASE FOLDER
REM ----------------------------------------

if not exist release mkdir release

echo.
echo Copying build files...

xcopy /E /I /Y dist\ release\

:END

echo.
echo ========================================
echo BUILD COMPLETE
echo ========================================
echo.

echo Your EXE build is ready.
echo.

pause
