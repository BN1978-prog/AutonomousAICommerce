from pathlib import Path

p = Path("app/exploration_engine_v2.py")
text = p.read_text(encoding="utf-8-sig")

if "from app.alert_dispatcher import notify" not in text:
    text = "from app.alert_dispatcher import notify\n" + text

marker = 'print("Products:",len(products))'

insert = '''
try:
    if winners:
        top = winners[0]
        sku = top.get("sku","unknown")
        score = top.get("score","unknown")
        notify("WINNER_PRODUCT", f"{sku} | score={score}")
except Exception as e:
    print("winner alert skipped:", e)

'''

if insert.strip() not in text and marker in text:
    text = text.replace(marker, insert + marker)

p.write_text(text, encoding="utf-8")

print("winner product alert connected")
