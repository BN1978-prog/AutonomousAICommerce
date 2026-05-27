import subprocess

commands = [
    "python -m app.autopilot_runner",
    "python -m app.control_panel",
]

for cmd in commands:
    print()
    print("=" * 60)
    print(cmd)
    print("=" * 60)
    subprocess.run(cmd, shell=True)
