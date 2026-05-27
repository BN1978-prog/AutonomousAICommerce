$ErrorActionPreference = "Stop"

Set-Location "C:\Users\omen\AutonomousAICommerce"

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = ".\app\logs\scheduled_runs"

if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
}

python -m app.autopilot_runner *>&1 | Tee-Object "$logDir\autopilot_$stamp.log"
