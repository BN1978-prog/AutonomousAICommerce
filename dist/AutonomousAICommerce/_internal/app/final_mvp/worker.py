import asyncio
import os
from datetime import datetime
from app.final_mvp.product_pipeline import ProductFinder
from app.final_mvp.governor import Governor
from app.final_mvp.db import SessionLocal, init_db, Opportunity, AutonomousEvent

class WorkerState:
    enabled = False
    running = False
    cycle_count = 0
    last_run_at = None
    last_message = "idle"

    @classmethod
    def dict(cls):
        return {
            "enabled": cls.enabled,
            "running": cls.running,
            "cycle_count": cls.cycle_count,
            "last_run_at": cls.last_run_at,
            "last_message": cls.last_message,
        }

async def run_one_cycle(keyword: str = "pet", max_cost: float = 50):
    init_db()
    finder = ProductFinder()
    governor = Governor()
    results = finder.find(keyword=keyword, max_cost=max_cost)

    db = SessionLocal()
    saved = 0
    approved = 0
    try:
        for r in results[: int(os.getenv("MAX_PRODUCTS_PER_CYCLE", "3"))]:
            allowed, reason = governor.allow_action(
                estimated_spend=r["supplier_cost"] + r["shipping_cost"],
                margin_percent=r["margin_percent"],
                risk_score=r["risk_score"],
            )
            opp = Opportunity(
                sku=r["sku"],
                title=r["title"],
                supplier_cost=r["supplier_cost"],
                shipping_cost=r["shipping_cost"],
                expected_sale_price=r["expected_sale_price"],
                net_profit=r["net_profit"],
                margin_percent=r["margin_percent"],
                risk_score=r["risk_score"],
                opportunity_score=r["opportunity_score"],
                decision=("approved_dry_run" if allowed and r["decision"] == "approve" else r["decision"]),
            )
            db.add(opp)
            saved += 1
            if allowed and r["decision"] == "approve":
                approved += 1

        db.add(AutonomousEvent(
            event_type="cycle",
            message=f"Cycle completed. saved={saved}, approved={approved}",
            dry_run=governor.status()["dry_run"],
        ))
        db.commit()
    finally:
        db.close()

    WorkerState.cycle_count += 1
    WorkerState.last_run_at = datetime.utcnow().isoformat() + "Z"
    WorkerState.last_message = f"Cycle completed. saved={saved}, approved={approved}"

    return {"saved": saved, "approved": approved, "results": results, "worker": WorkerState.dict()}

async def worker_loop():
    WorkerState.running = True
    try:
        while True:
            if WorkerState.enabled:
                await run_one_cycle()
            await asyncio.sleep(int(os.getenv("AUTONOMOUS_INTERVAL_SECONDS", "60")))
    finally:
        WorkerState.running = False
