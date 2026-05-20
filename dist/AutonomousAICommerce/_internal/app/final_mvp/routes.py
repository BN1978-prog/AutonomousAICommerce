import asyncio
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.final_mvp.db import db_status, init_db, SessionLocal, Opportunity, AutonomousEvent
from app.final_mvp.product_pipeline import ProductFinder
from app.final_mvp.worker import WorkerState, run_one_cycle, worker_loop
from app.final_mvp.governor import Governor
from app.final_mvp.shopify import ShopifyDraftService

router = APIRouter()
_worker_task = None

class ShopifyDraftRequest(BaseModel):
    title: str
    description: str = ""
    price: float = Field(gt=0)

@router.get("/status")
def status():
    return {
        "final_mvp": "installed",
        "governor": Governor().status(),
        "worker": WorkerState.dict(),
    }

@router.get("/db/status")
def database_status():
    return db_status()

@router.get("/opportunities/run")
def run_opportunities(keyword: str = "pet", max_cost: float = 50):
    init_db()
    finder = ProductFinder()
    results = finder.find(keyword=keyword, max_cost=max_cost)

    db = SessionLocal()
    try:
        for r in results:
            db.add(Opportunity(
                sku=r["sku"],
                title=r["title"],
                supplier_cost=r["supplier_cost"],
                shipping_cost=r["shipping_cost"],
                expected_sale_price=r["expected_sale_price"],
                net_profit=r["net_profit"],
                margin_percent=r["margin_percent"],
                risk_score=r["risk_score"],
                opportunity_score=r["opportunity_score"],
                decision=r["decision"],
            ))
        db.commit()
    finally:
        db.close()

    return {"count": len(results), "results": results}

@router.post("/autonomous/cycle")
async def autonomous_cycle(keyword: str = "pet", max_cost: float = 50):
    return await run_one_cycle(keyword=keyword, max_cost=max_cost)

@router.post("/autonomous/start")
async def start_worker():
    global _worker_task
    WorkerState.enabled = True
    if _worker_task is None or _worker_task.done():
        _worker_task = asyncio.create_task(worker_loop())
    return WorkerState.dict()

@router.post("/autonomous/stop")
def stop_worker():
    WorkerState.enabled = False
    return WorkerState.dict()

@router.get("/events")
def events(limit: int = 20):
    init_db()
    db = SessionLocal()
    try:
        rows = db.query(AutonomousEvent).order_by(AutonomousEvent.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "event_type": r.event_type,
                "message": r.message,
                "dry_run": r.dry_run,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    finally:
        db.close()

@router.post("/shopify/create-draft")
async def create_shopify_draft(req: ShopifyDraftRequest):
    service = ShopifyDraftService()
    return await service.create_draft_product(req.title, req.description, req.price)
