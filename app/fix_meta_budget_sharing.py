from pathlib import Path

p=Path("app/meta_live_executor.py")
text=p.read_text(encoding="utf-8")

old='''
        "special_ad_categories": "[]",
'''

new='''
        "special_ad_categories": "[]",
        "is_adset_budget_sharing_enabled": "false",
'''

if "is_adset_budget_sharing_enabled" not in text:
    text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("Meta adset budget sharing flag added")
