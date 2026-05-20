def detect_duplicate_skus(products:list):
    seen={}
    duplicates=set()

    for p in products:

        sku = (
            p.get("sku")
            or (
                (p.get("variants") or [{}])[0].get("sku")
                if p.get("variants")
                else None
            )
        )

        if not sku:
            continue

        if sku in seen:
            duplicates.add(sku)

        seen[sku]=seen.get(sku,0)+1

    return duplicates
