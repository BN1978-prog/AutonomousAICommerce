@echo off

cd /d C:\Users\omen\AutonomousAICommerce

start http://127.0.0.1:8010/dashboard

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8010

pause
