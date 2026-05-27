import subprocess

commands = [
    "python -m app.master_system_health",
    "python -m app.autopilot_report",
    "python -m app.crm_readiness_summary",
    "python -m app.meta_launch_readiness",
    "python -m app.google_access_status",
    "python -m app.amazon_connection_status",
    "python -m app.channel_health_report",
    "python -m app.system_status_report",
]

for cmd in commands:
    print()
    print("=" * 60)
    print(cmd)
    print("=" * 60)
    subprocess.run(cmd, shell=True)
