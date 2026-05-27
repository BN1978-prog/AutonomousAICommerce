from pathlib import Path

p=Path("app/meta_live_executor.py")
text=p.read_text(encoding="utf-8")

old='''
        url = f"https://graph.facebook.com/{API_VERSION}/act_{AD_ACCOUNT_ID}/campaigns"
'''

new='''
        account_id = AD_ACCOUNT_ID
        if not account_id.startswith("act_"):
            account_id = f"act_{account_id}"

        url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/campaigns"
'''

text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("Meta account id normalization fixed")
