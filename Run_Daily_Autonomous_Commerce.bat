cd /d C:\Users\omen\AutonomousAICommerce
if not exist app\logs\daily_runs mkdir app\logs\daily_runs

for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set today=%%d-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set now=%%a-%%b

python -m app.daily_run > app\logs\daily_runs\daily_run_%today%_%now%.txt 2>&1

type app\logs\daily_runs\daily_run_%today%_%now%.txt
pause
