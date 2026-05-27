from pathlib import Path

p=Path("app/exploration_engine_v2.py")
text=p.read_text(encoding="utf-8")

old='final_score=score+boost'

new='''
winner=False

if sales>=3:
    winner=True
    boost=max(boost-10,0)

final_score=score+boost
'''

if "winner=True" not in text:
    text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("Winner protection added")
