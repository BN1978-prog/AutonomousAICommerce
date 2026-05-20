from pathlib import Path

p=Path("app/product_hunter/service.py")
s=p.read_text(encoding="utf-8")

old='''        for p in promoted[:10]:
            print(
                p["sku"],
                "score=",p["score"],
                "price=",p["price"]
            )

        return promoted'''

new='''        for p in promoted[:10]:
            print(
                p["sku"],
                "score=",p["score"],
                "price=",p["price"]
            )

        import json
        from pathlib import Path
        out = Path("app/logs/hunter_promoted.json")
        out.write_text(json.dumps(promoted, indent=2), encoding="utf-8")
        print("SAVED:", out)

        return promoted'''

s=s.replace(old,new)
p.write_text(s,encoding="utf-8")
print("hunter promoted log added")
