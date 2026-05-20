from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.upgrade.ai_scoring import score_product_opportunity, ProductOpportunityInput
from app.upgrade.worker_state import worker_state
from app.upgrade.shopify_client import ShopifyClient
from app.upgrade.supplier_sandbox import SupplierSandboxClient

router = APIRouter()

class ScoreRequest(BaseModel):
    title: str
    supplier_cost: float = Field(gt=0)
    expected_sale_price: float = Field(gt=0)
    shipping_cost: float = Field(ge=0, default=0)
    platform_fee_percent: float = Field(ge=0, le=100, default=12)
    estimated_return_rate_percent: float = Field(ge=0, le=100, default=5)
    demand_score: float = Field(ge=0, le=100, default=50)
    competition_score: float = Field(ge=0, le=100, default=50)
    supplier_trust_score: float = Field(ge=0, le=100, default=80)

@router.get("/status")
def upgrade_status():
    return {
        "upgrade": "installed",
        "worker": worker_state.to_dict(),
        "modules": [
            "shopify_client",
            "supplier_sandbox",
            "ai_scoring",
            "background_worker",
            "postgres_ready_config",
        ],
    }

@router.post("/score-product")
def score_product(req: ScoreRequest):
    result = score_product_opportunity(ProductOpportunityInput(**req.model_dump()))
    return result.model_dump()

@router.post("/worker/start")
def start_worker():
    worker_state.enabled = True
    return worker_state.to_dict()

@router.post("/worker/stop")
def stop_worker():
    worker_state.enabled = False
    return worker_state.to_dict()

@router.get("/supplier/search")
def supplier_search(q: str = "pet bowl", max_cost: float = 50):
    supplier = SupplierSandboxClient()
    return supplier.search_products(q, max_cost=max_cost)

@router.get("/shopify/status")
def shopify_status():
    client = ShopifyClient.from_env()
    return client.status()
