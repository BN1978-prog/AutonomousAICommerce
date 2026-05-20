import json
from pathlib import Path

hunter=Path("app/logs/hunter_promoted.json")
imports=Path("app/logs/imported_skus.json")

print("=== HUNTER ===")
if hunter.exists():
    print(hunter.read_text(encoding="utf-8"))
else:
    print("missing")

print()
print("=== IMPORTS ===")
if imports.exists():
    print(imports.read_text(encoding="utf-8"))
else:
    print("missing")
