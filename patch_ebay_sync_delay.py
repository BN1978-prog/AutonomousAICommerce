from pathlib import Path

p=Path("app/publish_ebay_from_imports.py")
s=p.read_text(encoding="utf-8")

old='''print(json.dumps(inv, indent=2))

        offer = ebay_create_offer('''

new='''print(json.dumps(inv, indent=2))

        import time
        print("Waiting for eBay inventory sync...")
        time.sleep(8)

        offer = ebay_create_offer('''

p.write_text(s.replace(old,new),encoding="utf-8")

print("SYNC DELAY ADDED")
