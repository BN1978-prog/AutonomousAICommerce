from pathlib import Path

p=Path("app/product_hunter/service.py")
s=p.read_text(encoding="utf-8")

insert = '''

    async def hunt_and_promote(self, request: HunterRequest, current_daily_spend: float = 0.0):
        result = await self.hunt(request, current_daily_spend)

        promoted=[]

        for opp in result.opportunities:

            if (
                opp.opportunity_score >= 80
                and opp.decision.status.value != "rejected"
            ):
                promoted.append({
                    "sku": getattr(opp.source_product,"sku","unknown"),
                    "score": opp.opportunity_score,
                    "price": opp.recommended_sale_price
                })

        print("\\n=== AI PRODUCT HUNTER ===")
        print("FOUND:",len(result.opportunities))
        print("PROMOTED:",len(promoted))

        for p in promoted[:10]:
            print(
                p["sku"],
                "score=",p["score"],
                "price=",p["price"]
            )

        return promoted
'''

marker='return [\n            f"Opportunity score: {score}",'

if insert not in s:
    s += insert

p.write_text(s,encoding="utf-8")
print("hunter auto-promote added")
