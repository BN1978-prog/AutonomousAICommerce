from pathlib import Path

p=Path("app/exploration_engine_v2.py")
text=p.read_text(encoding="utf-8")

anchor='''
OUT.write_text(
'''

insert='''
try:
    winners = report.get("top_winners", [])
    if winners:
        top = winners[0]
        sku = top.get("sku", "unknown")
        score = top.get("score", "unknown")
        notify("WINNER_PRODUCT", f"{sku} | score={score}")
        print(f"WINNER ALERT SENT: {sku} score={score}")
except Exception as e:
    print("winner alert skipped:", e)

'''

if "WINNER ALERT SENT" not in text:
    text=text.replace(anchor, insert + anchor)

p.write_text(text,encoding="utf-8")

print("winner notify block inserted")
