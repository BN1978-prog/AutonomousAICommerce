from pathlib import Path

p=Path("app/exploration_engine_v2.py")
text=p.read_text(encoding="utf-8")

old='''
notify("WINNER_PRODUCT", f"{sku} | score={score}")
'''

new='''
notify("WINNER_PRODUCT", f"{sku} | score={score}")
print(f"WINNER ALERT SENT: {sku} score={score}")
'''

if old in text:
    text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("winner alert logging enabled")
