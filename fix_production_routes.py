from pathlib import Path
import shutil

ROOT = Path(r"C:\Users\omen\AutonomousAICommerce")
MAIN = ROOT / "app" / "main.py"

if not MAIN.exists():
    raise SystemExit("ERROR: app/main.py not found")

backup = ROOT / "app" / "main.py.bak_fix_production"
if not backup.exists():
    shutil.copy2(MAIN, backup)

text = MAIN.read_text(encoding="utf-8")

import_line = "from app.production.routes import router as production_router"
include_line = 'app.include_router(production_router, prefix="/production", tags=["production"])'

if import_line not in text:
    lines = text.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            insert_at = i + 1
    lines.insert(insert_at, import_line)
    text = "\n".join(lines)

if include_line not in text:
    text = text.rstrip() + "\n\n" + include_line + "\n"

MAIN.write_text(text, encoding="utf-8")

print("Production routes patched successfully.")
print("Backup saved as:", backup)