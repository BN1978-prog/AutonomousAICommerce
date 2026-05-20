import json
from pathlib import Path

p=Path("app/auto_disable_skus.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
'    score = data.get("last_score",0)',
'    score = data.get("last_score", None)'
)

s=s.replace(
'    if score < 60:',
'    if score is not None and score < 60:'
)

p.write_text(s,encoding="utf-8")
print("auto disable score logic fixed")
