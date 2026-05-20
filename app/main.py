from dotenv import load_dotenv
load_dotenv()
import requests
def load_env_local():
    import os
    from pathlib import Path

    env_file = Path(".env.local")

    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env_local()

from fastapi import FastAPI
from app.commerce.routes import router as commerce_router
from fastapi.responses import HTMLResponse
from app.commerce.routes import router as commerce_router
from fastapi.staticfiles import StaticFiles
from app.commerce.routes import router as commerce_router
from app.core.config import get_settings
from app.schemas.decision import CommerceDecision
from app.schemas.product import ProductCandidate
from app.services.governor import AIGovernor
from app.suppliers.registry import SupplierRegistry
from app.suppliers.schemas import SupplierProduct, SupplierSearchQuery
from app.marketplaces.registry import MarketplaceRegistry
from app.marketplaces.schemas import ListingDraft, ListingResult, MarketplaceName, PriceUpdateRequest, MarketplaceOrder
from app.product_hunter.schemas import HunterRequest, HunterResponse
from app.product_hunter.service import ProductHunterService
from app.finance.schemas import AdvancedEvaluationRequest, ScenarioResult
from app.finance.advanced_profit_engine import AdvancedProfitEngine
from app.services.advanced_governor import AdvancedAIGovernor
from app.schemas.decision import AdvancedCommerceDecision
from app.listings.schemas import ListingGenerationRequest, GeneratedListing
from app.listings.generator import AutoListingGenerator
from app.fulfillment.schemas import FulfillmentRequest, FulfillmentResult
from app.fulfillment.service import FulfillmentService
from app.shipping.registry import ShippingRegistry
from app.shipping.schemas import CarrierName, Shipment, ShipmentRequest, ShippingRate, ShippingRateRequest, TrackingEvent
from app.support.schemas import SupportClassification, SupportReply, SupportRequest
from app.support.service import CustomerSupportAI
from app.adaptation.schemas import AdaptationRequest, LearningSummary
from app.adaptation.engine import SelfLearningEngine
from app.dashboard.schemas import AutonomyControls, DashboardMetrics, DashboardStatus
from app.dashboard.service import DashboardService

from app.automation.schemas import SemiAutoRunRequest, SemiAutoRunResult
from app.automation.service import SemiAutoCommerceService
from app.production.routes import router as production_router
from app.final_mvp.routes import router as final_mvp_router
from app.shopify_automation.routes import router as shopify_automation_router


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.11.0")
supplier_registry = SupplierRegistry()
marketplace_registry = MarketplaceRegistry()
product_hunter_service = ProductHunterService(settings, supplier_registry)
fulfillment_service = FulfillmentService(settings, supplier_registry)
shipping_registry = ShippingRegistry()
support_ai = CustomerSupportAI()
self_learning_engine = SelfLearningEngine()
dashboard_service = DashboardService(settings)
semi_auto_service = SemiAutoCommerceService(settings, dashboard_service, supplier_registry, marketplace_registry)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/evaluate", response_model=CommerceDecision)
def evaluate_product(product: ProductCandidate, current_daily_spend: float = 0.0) -> CommerceDecision:
    governor = AIGovernor(settings)
    return governor.evaluate(product, current_daily_spend=current_daily_spend)


@app.post("/suppliers/search", response_model=list[SupplierProduct])
async def search_suppliers(query: SupplierSearchQuery) -> list[SupplierProduct]:
    return await supplier_registry.search_all(query)


@app.get("/marketplaces", response_model=list[str])
def list_marketplaces() -> list[str]:
    return marketplace_registry.list_names()


@app.post("/marketplaces/{marketplace}/listings", response_model=ListingResult)
async def publish_listing(marketplace: MarketplaceName, draft: ListingDraft) -> ListingResult:
    client = marketplace_registry.get(marketplace)
    return await client.publish_listing(draft)


@app.patch("/marketplaces/{marketplace}/listings/price", response_model=ListingResult)
async def update_listing_price(marketplace: MarketplaceName, request: PriceUpdateRequest) -> ListingResult:
    client = marketplace_registry.get(marketplace)
    return await client.update_price(request)


@app.get("/marketplaces/{marketplace}/orders", response_model=list[MarketplaceOrder])
async def fetch_marketplace_orders(marketplace: MarketplaceName) -> list[MarketplaceOrder]:
    client = marketplace_registry.get(marketplace)
    return await client.fetch_open_orders()


@app.post("/hunter/opportunities", response_model=HunterResponse)
async def hunt_product_opportunities(request: HunterRequest, current_daily_spend: float = 0.0) -> HunterResponse:
    return await product_hunter_service.hunt(request, current_daily_spend=current_daily_spend)


@app.post("/risk/advanced-evaluate", response_model=AdvancedCommerceDecision)
def advanced_evaluate(request: AdvancedEvaluationRequest, current_daily_spend: float = 0.0) -> AdvancedCommerceDecision:
    governor = AdvancedAIGovernor(settings)
    return governor.evaluate(request, current_daily_spend=current_daily_spend)


@app.post("/profit/scenarios", response_model=list[ScenarioResult])
def profit_scenarios(request: AdvancedEvaluationRequest) -> list[ScenarioResult]:
    engine = AdvancedProfitEngine()
    return engine.scenarios(
        sale_price=request.expected_sale_price,
        supplier_cost=request.supplier_cost,
        supplier_shipping=request.supplier_shipping,
        fee_model=request.fee_model,
        cost_assumptions=request.cost_assumptions,
    )


@app.post("/listings/generate", response_model=GeneratedListing)
def generate_listing(request: ListingGenerationRequest) -> GeneratedListing:
    generator = AutoListingGenerator()
    return generator.generate(request)


@app.post("/fulfillment/process", response_model=FulfillmentResult)
async def process_fulfillment(request: FulfillmentRequest, current_daily_spend: float = 0.0) -> FulfillmentResult:
    return await fulfillment_service.fulfill(request, current_daily_spend=current_daily_spend)


@app.get("/shipping/carriers", response_model=list[str])
def list_shipping_carriers() -> list[str]:
    return shipping_registry.list_names()


@app.post("/shipping/rates", response_model=list[ShippingRate])
async def quote_shipping_rates(request: ShippingRateRequest) -> list[ShippingRate]:
    return await shipping_registry.quote_all(request)


@app.post("/shipping/shipments", response_model=Shipment)
async def create_shipping_shipment(request: ShipmentRequest) -> Shipment:
    return await shipping_registry.create_shipment(request)


@app.get("/shipping/{carrier}/track/{tracking_number}", response_model=list[TrackingEvent])
async def track_shipping(carrier: CarrierName, tracking_number: str) -> list[TrackingEvent]:
    return await shipping_registry.track(carrier, tracking_number)


@app.post("/support/classify", response_model=SupportClassification)
def classify_support_message(request: SupportRequest) -> SupportClassification:
    return support_ai.classify(request)


@app.post("/support/reply", response_model=SupportReply)
def draft_support_reply(request: SupportRequest) -> SupportReply:
    return support_ai.draft_reply(request)


@app.post("/adaptation/analyze", response_model=LearningSummary)
def analyze_adaptation(request: AdaptationRequest) -> LearningSummary:
    return self_learning_engine.analyze(request)


@app.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard() -> str:
    with open("static/dashboard.html", "r", encoding="utf-8") as dashboard_file:
        return dashboard_file.read()


@app.get("/dashboard/status", response_model=DashboardStatus)
def dashboard_status() -> DashboardStatus:
    return dashboard_service.get_status()


@app.get("/dashboard/metrics", response_model=DashboardMetrics)
def dashboard_metrics() -> DashboardMetrics:
    return dashboard_service.get_metrics()


@app.put("/dashboard/controls", response_model=AutonomyControls)
def dashboard_controls(controls: AutonomyControls) -> AutonomyControls:
    return dashboard_service.update_controls(controls)





@app.get("/dashboard/report-preview")
def dashboard_report_preview(path: str):
    from pathlib import Path

    allowed_roots = [
        Path("app/logs").resolve(),
        Path("app/reports").resolve(),
        Path("reports").resolve(),
        Path("data").resolve(),
        Path("app/data").resolve()
    ]

    file_path = Path(path).resolve()

    if not any(str(file_path).startswith(str(root)) for root in allowed_roots):
        return {"error": "Path is not allowed."}

    if not file_path.exists() or not file_path.is_file():
        return {"error": "Report file not found."}

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return {
            "name": file_path.name,
            "path": str(file_path),
            "content": content[:20000]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/dashboard/reports")
def dashboard_reports():
    from pathlib import Path

    roots = [
        Path("app/logs"),
        Path("app/reports"),
        Path("reports"),
        Path("data"),
        Path("app/data")
    ]

    found = []

    for root in roots:
        if root.exists():
            for pattern in ["*.json", "*.txt", "*.csv"]:
                for file in root.rglob(pattern):
                    try:
                        found.append({
                            "name": file.name,
                            "path": str(file),
                            "size": file.stat().st_size,
                            "modified": file.stat().st_mtime
                        })
                    except Exception:
                        pass

    found = sorted(found, key=lambda x: x["modified"], reverse=True)[:30]

    return {"reports": found}

@app.get("/dashboard/logs")
def dashboard_logs():
    from pathlib import Path

    logs_dir = Path("app/logs/daily_runs")

    if not logs_dir.exists():
        return {"logs": ["Logs directory not found."]}

    files = sorted(
        logs_dir.glob("*.txt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return {"logs": ["No log files found."]}

    latest = files[0]

    try:
        content = latest.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()[-120:]
        return {
            "file": latest.name,
            "logs": lines
        }
    except Exception as e:
        return {"logs": [str(e)]}


@app.post("/dashboard/daily-run")
def dashboard_daily_run():
    import subprocess
    import sys
    from pathlib import Path
    from datetime import datetime

    logs_dir = Path("app/logs/daily_runs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / ("dashboard_daily_run_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "app.daily_run"],
            capture_output=True,
            text=True,
            timeout=300
        )

        output = (result.stdout or "") + "\n" + (result.stderr or "")
        log_file.write_text(output, encoding="utf-8", errors="ignore")

        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "log_file": str(log_file),
            "output": output[-12000:]
        }

    except Exception as e:
        log_file.write_text(str(e), encoding="utf-8", errors="ignore")
        return {
            "ok": False,
            "error": str(e),
            "log_file": str(log_file)
        }

@app.post("/automation/semi-auto/run", response_model=SemiAutoRunResult)
async def run_semi_auto_workflow(request: SemiAutoRunRequest) -> SemiAutoRunResult:
    return await semi_auto_service.run(request)

app.include_router(production_router, prefix="/production", tags=["production"])

app.include_router(final_mvp_router, prefix="/final", tags=["final-mvp"])
app.include_router(shopify_automation_router, prefix="/shopify-auto", tags=["shopify-auto"])











@app.get("/dashboard/real-kpis")
def dashboard_real_kpis():
    from pathlib import Path
    import json

    logs = Path("app/logs")

    imported_count = 0
    blocked_count = 0
    image_failed_count = 0
    stock_count = 0
    out_of_stock_count = 0

    imported_file = logs / "imported_skus.json"
    blocked_file = logs / "blocked_products.json"
    stock_file = logs / "stock_state.json"

    try:
        if imported_file.exists():
            imported = json.loads(imported_file.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(imported, dict):
                imported_count = len(imported)
                image_failed_count = len([
                    sku for sku, info in imported.items()
                    if isinstance(info, dict) and info.get("image_status") == "failed"
                ])
    except Exception:
        pass

    try:
        if blocked_file.exists():
            blocked = json.loads(blocked_file.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(blocked, list):
                blocked_count = len(blocked)
                out_of_stock_count = len([
                    item for item in blocked
                    if "out of stock" in " ".join(item.get("issues", []))
                ])
    except Exception:
        pass

    try:
        if stock_file.exists():
            stock = json.loads(stock_file.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(stock, dict):
                stock_count = len(stock)
    except Exception:
        pass

    return {
        "imported_skus": imported_count,
        "blocked_products": blocked_count,
        "image_failed": image_failed_count,
        "tracked_stock_skus": stock_count,
        "out_of_stock": out_of_stock_count
    }

@app.get("/dashboard/data-summary")
def dashboard_data_summary():
    from pathlib import Path
    import json
    import csv

    roots = [
        Path("app/logs"),
        Path("app/data"),
        Path("data"),
        Path("reports"),
    ]

    result = {
        "imported_products": [],
        "blocked_products": [],
        "stock_issues": [],
        "image_issues": []
    }

    buckets = {
        "imported_products": ["imported_skus"],
        "blocked_products": ["blocked"],
        "stock_issues": ["stock", "inventory"],
        "image_issues": ["image"]
    }

    def read_file(file):
        try:
            if file.suffix.lower() == ".json":
                data = json.loads(file.read_text(encoding="utf-8", errors="ignore"))
                return data if isinstance(data, list) else [data]

            if file.suffix.lower() == ".csv":
                with file.open("r", encoding="utf-8", errors="ignore") as f:
                    return list(csv.DictReader(f))

            return file.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception as e:
            return [{"error": str(e), "file": str(file)}]

    for root in roots:
        if not root.exists():
            continue

        for file in root.rglob("*"):
            if file.suffix.lower() not in [".json", ".csv", ".txt"]:
                continue

            name = file.name.lower()

            for bucket, terms in buckets.items():
                if (
                    (bucket == "imported_products" and "imported_skus" in name)
                    or (bucket != "imported_products" and any(term in name for term in terms))
                ):
                    data = read_file(file)
                    result[bucket].append({
                        "file": str(file),
                        "count": len(data),
                        "sample": data[:5]
                    })

    return result






@app.get("/dashboard/api-readiness")
def dashboard_api_readiness():
    import os

    def masked_status(key):
        value = os.getenv(key, "")
        return {
            "configured": bool(value),
            "length": len(value) if value else 0,
            "preview": (value[:4] + "..." + value[-4:]) if len(value) > 8 else "MISSING"
        }

    return {
        "shopify_store_url": bool(os.getenv("SHOPIFY_STORE_URL")),
        "shopify_access_token": masked_status("SHOPIFY_ACCESS_TOKEN"),
        "openai_api_key": masked_status("OPENAI_API_KEY"),
        "supplier_api_key": masked_status("SUPPLIER_API_KEY"),
        "dry_run": os.getenv("DRY_RUN", "true"),
        "autonomy_enabled": os.getenv("AUTONOMY_ENABLED", "false"),
        "emergency_stop": os.getenv("EMERGENCY_STOP", "false")
    }



@app.get("/dashboard/cj-test")
def dashboard_cj_test():
    import os
    import requests

    api_key = os.getenv("SUPPLIER_API_KEY", "")

    if not api_key:
        return {
            "ok": False,
            "message": "SUPPLIER_API_KEY is missing."
        }

    try:
        url = "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken"

        response = requests.post(
            url,
            json={
                "email": "",
                "password": "",
                "apiKey": api_key
            },
            timeout=20
        )

        try:
            payload = response.json()
        except Exception:
            payload = {}

        data = payload.get("data", {}) if isinstance(payload, dict) else {}

        return {
            "ok": payload.get("code") == 200 if isinstance(payload, dict) else response.status_code == 200,
            "status_code": response.status_code,
            "message": payload.get("message", "unknown") if isinstance(payload, dict) else "unknown",
            "open_id": data.get("openId"),
            "access_token_configured": bool(data.get("accessToken")),
            "access_token_expiry": data.get("accessTokenExpiryDate"),
            "refresh_token_configured": bool(data.get("refreshToken")),
            "mode": os.getenv("SUPPLIER_MODE", "sandbox"),
            "dry_run": os.getenv("DRY_RUN", "true")
        }

    except Exception as e:
        return {
            "ok": False,
            "message": str(e),
            "mode": os.getenv("SUPPLIER_MODE", "sandbox"),
            "dry_run": os.getenv("DRY_RUN", "true")
        }




@app.get("/dashboard/cj-products")
def dashboard_cj_products(keyword: str = "pet", page: int = 1, size: int = 10):
    import os
    import requests

    api_key = os.getenv("SUPPLIER_API_KEY", "")

    if not api_key:
        return {"ok": False, "message": "SUPPLIER_API_KEY is missing.", "products": []}

    try:
        token_response = requests.post(
            "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken",
            json={"email": "", "password": "", "apiKey": api_key},
            timeout=20
        )

        token_payload = token_response.json()
        access_token = (token_payload.get("data") or {}).get("accessToken")

        if not access_token:
            return {
                "ok": False,
                "message": "Could not get CJ access token.",
                "status_code": token_response.status_code,
                "products": []
            }

        product_response = requests.get(
            "https://developers.cjdropshipping.com/api2.0/v1/product/listV2",
            headers={"CJ-Access-Token": access_token},
            params={
                "page": max(1, page),
                "size": min(max(1, size), 20),
                "keyWord": keyword
            },
            timeout=30
        )

        payload = product_response.json()
        data = payload.get("data") or {}

        raw_products = []

        for block in data.get("content", []):
            if isinstance(block, dict):
                raw_products.extend(block.get("productList", []) or [])

        products = []

        for item in raw_products[:20]:
            products.append({
                "pid": item.get("id"),
                "sku": item.get("sku"),
                "title": item.get("nameEn"),
                "image": item.get("bigImage"),
                "price": item.get("sellPrice") or item.get("nowPrice"),
                "category": item.get("threeCategoryName") or item.get("twoCategoryName") or item.get("oneCategoryName"),
                "listed_num": item.get("listedNum"),
                "inventory": item.get("warehouseInventoryNum"),
                "source": "CJdropshipping"
            })

        return {
            "ok": payload.get("code") == 200,
            "message": payload.get("message"),
            "keyword": keyword,
            "total_records": data.get("totalRecords"),
            "total_pages": data.get("totalPages"),
            "count": len(products),
            "products": products,
            "dry_run": os.getenv("DRY_RUN", "true")
        }

    except Exception as e:
        return {
            "ok": False,
            "message": str(e),
            "keyword": keyword,
            "products": [],
            "dry_run": os.getenv("DRY_RUN", "true")
        }
@app.get("/dashboard/cj-products-raw")
def dashboard_cj_products_raw(keyword: str = "pet", size: int = 3):
    import os
    import requests

    api_key = os.getenv("SUPPLIER_API_KEY", "")

    token_response = requests.post(
        "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken",
        json={"email": "", "password": "", "apiKey": api_key},
        timeout=20
    )

    access_token = token_response.json().get("data", {}).get("accessToken")

    product_response = requests.get(
        "https://developers.cjdropshipping.com/api2.0/v1/product/listV2",
        headers={"CJ-Access-Token": access_token},
        params={
            "page": 1,
            "size": size,
            "keyWord": keyword
        },
        timeout=30
    )

    return product_response.json()



@app.get("/dashboard/cj-products-v2")
def dashboard_cj_products_v2(keyword: str = "pet", page: int = 1, size: int = 10):
    import os
    import requests

    api_key = os.getenv("SUPPLIER_API_KEY", "")

    if not api_key:
        return {"ok": False, "message": "SUPPLIER_API_KEY is missing.", "products": []}

    token_response = requests.post(
        "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken",
        json={"email": "", "password": "", "apiKey": api_key},
        timeout=20
    )

    access_token = token_response.json().get("data", {}).get("accessToken")

    if not access_token:
        return {"ok": False, "message": "Could not get CJ access token.", "products": []}

    product_response = requests.get(
        "https://developers.cjdropshipping.com/api2.0/v1/product/listV2",
        headers={"CJ-Access-Token": access_token},
        params={
            "page": max(1, page),
            "size": min(max(1, size), 20),
            "keyWord": keyword
        },
        timeout=30
    )

    payload = product_response.json()
    data = payload.get("data") or {}

    raw_products = []

    for block in data.get("content", []):
        raw_products.extend(block.get("productList", []) or [])

    products = []

    for item in raw_products[:20]:
        products.append({
            "pid": item.get("id"),
            "sku": item.get("sku"),
            "title": item.get("nameEn"),
            "image": item.get("bigImage"),
            "price": item.get("sellPrice"),
            "category": item.get("threeCategoryName") or item.get("twoCategoryName") or item.get("oneCategoryName"),
            "listed_num": item.get("listedNum"),
            "inventory": item.get("warehouseInventoryNum"),
            "source": "CJdropshipping"
        })

    return {
        "ok": payload.get("code") == 200,
        "message": payload.get("message"),
        "keyword": keyword,
        "total_records": data.get("totalRecords"),
        "total_pages": data.get("totalPages"),
        "count": len(products),
        "products": products,
        "dry_run": os.getenv("DRY_RUN", "true")
    }


@app.get("/dashboard/ai-analyze-cj-products")
def dashboard_ai_analyze_cj_products(keyword: str = "pet", size: int = 5):
    import os
    import json
    import re
    from pathlib import Path

    openai_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not openai_key:
        return {"ok": False, "message": "OPENAI_API_KEY is missing.", "analysis": []}

    cj = dashboard_cj_products_v2(keyword=keyword, page=1, size=size)

    products = cj.get("products", [])

    if not products:
        return {"ok": False, "message": "No CJ products found.", "analysis": []}

    prompt = {
        "task": "Analyze CJdropshipping products for Shopify dropshipping draft listing suitability.",
        "rules": [
            "Return JSON only.",
            "Do not recommend unsafe, illegal, medical, adult, or trademark-risk products.",
            "Score each product from 0 to 100.",
            "Estimate risk: low, medium, high.",
            "Suggest Shopify title, short description, tags, and recommended action.",
            "Assume DRY_RUN=true and no live publishing."
        ],
        "products": products
    }

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": "Bearer " + openai_key,
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "input": "Return strict JSON for this ecommerce analysis:\n" + json.dumps(prompt, ensure_ascii=False),
            "temperature": 0.2
        },
        timeout=60
    )

    try:
        payload = response.json()
    except Exception:
        return {
            "ok": False,
            "status_code": response.status_code,
            "message": response.text[:1000],
            "analysis": []
        }

    output_text = ""

    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in ["output_text", "text"]:
                output_text += content.get("text", "")

    return {
        "ok": response.status_code in [200, 201],
        "status_code": response.status_code,
        "keyword": keyword,
        "products_checked": len(products),
        "raw_output": output_text,
        "dry_run": os.getenv("DRY_RUN", "true")
    }


@app.post("/dashboard/shopify-draft-from-ai")
def dashboard_shopify_draft_from_ai(payload: dict):
    import os
    import asyncio
    import json
    from pathlib import Path
    from datetime import datetime
    from app.final_mvp.shopify import ShopifyDraftService

    force_real = bool(payload.get("force_real"))
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true" and not force_real

    product = {
        "product": {
            "title": payload.get("shopify_title") or payload.get("title") or "AI Generated Product",
            "body_html": payload.get("description") or "AI generated Shopify draft product.",
            "vendor": "CJdropshipping",
            "status": "active" if (
                bool(payload.get("allow_publish")) and
                os.getenv("AUTOPUBLISH_ENABLED", "false").lower() == "true"
            ) else "draft",
            "tags": ", ".join(payload.get("tags", [])) if isinstance(payload.get("tags"), list) else str(payload.get("tags", "")),
            "images": [{"src": payload.get("image")}] if payload.get("image") else [],
            "variants": [
                {
                    "sku": payload.get("sku") or payload.get("pid") or "CJ-AI-DRAFT",
                    "price": str(payload.get("price") or "19.99"),
                    "inventory_quantity": int(payload.get("inventory") or 0)
                }
            ]
        }
    }

    sku = product["product"]["variants"][0]["sku"]
    duplicate = _shopify_find_product_by_sku(sku)

    if duplicate.get("ok"):
        existing = duplicate["product"]

        return {
            "ok": True,
            "duplicate_blocked": True,
            "message": f"SKU {sku} already exists",
            "product_id": existing.get("id"),
            "title": existing.get("title"),
            "status": existing.get("status")
        }


    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "message": "DRY_RUN enabled. Shopify draft payload generated only.",
            "payload": product
        }

    if force_real:
        import requests

        store = os.getenv("SHOPIFY_STORE_URL", "").strip().replace("https://", "").replace("http://", "").rstrip("/")
        token = os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip()
        api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01")

        response = requests.post(
            f"https://{store}/admin/api/{api_version}/products.json",
            headers={
                "X-Shopify-Access-Token": token,
                "Content-Type": "application/json"
            },
            json=product,
            timeout=30
        )

        try:
            result = {
                "dry_run": False,
                "created": response.status_code in [200, 201],
                "status_code": response.status_code,
                "response": response.json()
            }
        except Exception:
            result = {
                "dry_run": False,
                "created": False,
                "status_code": response.status_code,
                "response_text": response.text[:1000]
            }
    else:
        shopify = ShopifyDraftService()
        result = asyncio.run(shopify.create_draft_from_payload(product))

    log_dir = Path("app/logs/shopify_drafts")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / (datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json")
    log_file.write_text(json.dumps({
        "created_at": datetime.now().isoformat(),
        "force_real": force_real,
        "result": result,
        "payload": product
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "ok": True,
        "dry_run": False,
        "message": "Shopify draft creation attempted.",
        "result": result,
        "payload": product,
        "log_file": str(log_file)
    }
@app.post("/dashboard/autopilot-draft-run")
def dashboard_autopilot_draft_run(payload: dict):
    import json
    import re
    import os

    keywords = payload.get("keywords") or ["pet", "travel pet", "pet bowl"]
    max_per_keyword = int(payload.get("max_per_keyword", 3))
    min_score = int(payload.get("min_score", 80))

    results = []

    for keyword in keywords:
        cj_products_response = dashboard_cj_products_v2(keyword=keyword, page=1, size=max_per_keyword)
        cj_products = cj_products_response.get("products", [])

        ai = dashboard_ai_analyze_cj_products(keyword=keyword, size=max_per_keyword)
        raw = ai.get("raw_output", "")

        cleaned = raw.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(cleaned)
        except Exception:
            match = re.search(r"\{[\s\S]*\}", cleaned)
            parsed = json.loads(match.group(0)) if match else {"analysis": []}

        for idx, item in enumerate(parsed.get("analysis", [])):
            score = int(item.get("score") or 0)

            if score < min_score:
                results.append({
                    "keyword": keyword,
                    "sku": item.get("sku"),
                    "title": item.get("title"),
                    "score": score,
                    "action": "skipped_low_score"
                })
                continue

            original = next(
                (
                    p for p in cj_products
                    if p.get("sku") == item.get("sku") or p.get("pid") == item.get("pid")
                ),
                cj_products[idx] if idx < len(cj_products) else {}
            )

            raw_price = str(original.get("price") or "9.99")
            first_price = raw_price.split("--")[0].strip()

            try:
                price_multiplier = float(os.getenv("PRICE_MULTIPLIER", "3"))
                min_sell_price = float(os.getenv("MIN_SELL_PRICE", "9.99"))
                sale_price = max(float(first_price) * price_multiplier, min_sell_price)
            except Exception:
                sale_price = 9.99

            cost_price = float(first_price or 0)
            profit = sale_price - cost_price
            margin_percent = (profit / sale_price * 100) if sale_price > 0 else 0
            min_margin = float(os.getenv("MIN_MARGIN_PERCENT", "50"))

            if margin_percent < min_margin:
                results.append({
                    "keyword": keyword,
                    "sku": item.get("sku") or original.get("sku"),
                    "title": item.get("title") or original.get("title"),
                    "score": score,
                    "risk": risk,
                    "cost_price": cost_price,
                    "sale_price": round(sale_price, 2),
                    "margin_percent": round(margin_percent, 2),
                    "action": "skipped_low_margin"
                })
                continue

            draft_payload = {
                "pid": item.get("pid") or original.get("pid"),
                "sku": item.get("sku") or original.get("sku"),
                "title": item.get("title") or original.get("title"),
                "shopify_title": item.get("suggestions", {}).get("shopify_title"),
                "description": item.get("suggestions", {}).get("short_description"),
                "tags": item.get("suggestions", {}).get("tags", []),
                "price": f"{sale_price:.2f}",
                "inventory": original.get("inventory") or 0,
                "image": original.get("image"),
                "force_real": False
            }

            draft = dashboard_shopify_safe_create_or_update(draft_payload)

            results.append({
                "keyword": keyword,
                "sku": item.get("sku"),
                "title": item.get("title"),
                "score": score,
                "risk": item.get("risk"),
                "action": "draft_generated",
                "draft": draft
            })

    return {
        "ok": True,
        "mode": "autopilot_draft",
        "dry_run": os.getenv("DRY_RUN", "true"),
        "keywords": keywords,
        "min_score": min_score,
        "created_or_previewed": len([r for r in results if r.get("action") == "draft_generated"]),
        "results": results
    }





@app.post("/dashboard/autopilot-real-draft-run")
def dashboard_autopilot_real_draft_run(payload: dict):
    import os
    import json
    import re
    from pathlib import Path

    keywords = payload.get("keywords") or ["pet", "travel pet", "pet bowl"]
    max_per_keyword = int(payload.get("max_per_keyword", 3))
    min_score = int(payload.get("min_score", 85))
    max_real_drafts = int(payload.get("max_real_drafts", 3))

    created = 0
    results = []

    imported_file = Path("app/logs/imported_skus.json")
    imported_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        imported_skus = json.loads(imported_file.read_text(encoding="utf-8")) if imported_file.exists() else {}
    except Exception:
        imported_skus = {}

    for keyword in keywords:
        if created >= max_real_drafts:
            break

        cj_products_response = dashboard_cj_products_v2(keyword=keyword, page=1, size=max_per_keyword)
        cj_products = cj_products_response.get("products", [])

        ai = dashboard_ai_analyze_cj_products(keyword=keyword, size=max_per_keyword)
        cleaned = ai.get("raw_output", "").replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(cleaned)
        except Exception:
            match = re.search(r"\{[\s\S]*\}", cleaned)
            parsed = json.loads(match.group(0)) if match else {"analysis": []}

        for idx, item in enumerate(parsed.get("analysis", [])):
            if created >= max_real_drafts:
                break

            score = int(item.get("score") or 0)
            risk = str(item.get("risk") or "").lower()

            original = next(
                (
                    p for p in cj_products
                    if p.get("sku") == item.get("sku") or p.get("pid") == item.get("pid")
                ),
                cj_products[idx] if idx < len(cj_products) else {}
            )

            sku = item.get("sku") or original.get("sku")

            if sku in imported_skus:
                results.append({
                    "keyword": keyword,
                    "sku": sku,
                    "title": item.get("title") or original.get("title"),
                    "score": score,
                    "risk": risk,
                    "action": "skipped_duplicate_sku"
                })
                continue

            if score < min_score or risk != "low":
                results.append({
                    "keyword": keyword,
                    "sku": item.get("sku") or original.get("sku"),
                    "title": item.get("title") or original.get("title"),
                    "score": score,
                    "risk": risk,
                    "action": "skipped_safety_filter"
                })
                continue

            raw_price = str(original.get("price") or "9.99")
            first_price = raw_price.split("--")[0].strip()

            try:
                price_multiplier = float(os.getenv("PRICE_MULTIPLIER", "3"))
                min_sell_price = float(os.getenv("MIN_SELL_PRICE", "9.99"))
                sale_price = max(float(first_price) * price_multiplier, min_sell_price)
            except Exception:
                sale_price = 9.99

            cost_price = float(first_price or 0)
            profit = sale_price - cost_price
            margin_percent = (profit / sale_price * 100) if sale_price > 0 else 0
            min_margin = float(os.getenv("MIN_MARGIN_PERCENT", "50"))

            if margin_percent < min_margin:
                results.append({
                    "keyword": keyword,
                    "sku": item.get("sku") or original.get("sku"),
                    "title": item.get("title") or original.get("title"),
                    "score": score,
                    "risk": risk,
                    "cost_price": cost_price,
                    "sale_price": round(sale_price, 2),
                    "margin_percent": round(margin_percent, 2),
                    "action": "skipped_low_margin"
                })
                continue

            draft_payload = {
                "pid": item.get("pid") or original.get("pid"),
                "sku": item.get("sku") or original.get("sku"),
                "title": item.get("title") or original.get("title"),
                "shopify_title": item.get("suggestions", {}).get("shopify_title") or item.get("title") or original.get("title"),
                "description": item.get("suggestions", {}).get("short_description") or "AI generated Shopify draft product.",
                "tags": item.get("suggestions", {}).get("tags", []),
                "price": f"{sale_price:.2f}",
                "inventory": original.get("inventory") or 0,
                "image": original.get("image"),
                "force_real": True,
                "allow_publish": margin_percent >= float(os.getenv("AUTOPUBLISH_MIN_MARGIN", "70")),
                "allow_publish": margin_percent >= float(os.getenv("AUTOPUBLISH_MIN_MARGIN", "70"))
            }

            draft = dashboard_shopify_safe_create_or_update(draft_payload)

            product_id = (
                draft.get("result", {})
                .get("response", {})
                .get("product", {})
                .get("id")
            )

            if product_id and draft_payload.get("sku"):
                imported_skus[draft_payload["sku"]] = {
                    "product_id": product_id,
                    "status": "draft_created",
                    "source": "autopilot_real_draft"
                }

                imported_file.write_text(
                    json.dumps(imported_skus, indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )

            created += 1

            results.append({
                "keyword": keyword,
                "sku": draft_payload["sku"],
                "title": draft_payload["title"],
                "score": score,
                "risk": risk,
                "action": "real_shopify_draft_created",
                "cost_price": round(cost_price, 2),
                "sale_price": round(sale_price, 2),
                "margin_percent": round(margin_percent, 2),
                "profit": round(profit, 2),
                "draft": draft
            })

    return {
        "ok": True,
        "mode": "autopilot_real_draft",
        "created": created,
        "max_real_drafts": max_real_drafts,
        "min_score": min_score,
        "safety": {
            "publishing": "disabled",
            "supplier_purchase": "disabled",
            "shopify_status": "draft"
        },
        "results": results
    }




@app.get("/dashboard/shopify-test")
def dashboard_shopify_test():
    import os
    import requests

    store = os.getenv("SHOPIFY_STORE_URL", "").strip().replace("https://", "").replace("http://", "").rstrip("/")
    token = os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip()
    api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01")

    if not store or not token:
        return {
            "ok": False,
            "message": "SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN missing.",
            "store_configured": bool(store),
            "token_configured": bool(token),
            "dry_run": os.getenv("DRY_RUN", "true")
        }

    response = requests.get(
        f"https://{store}/admin/api/{api_version}/shop.json",
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        },
        timeout=20
    )

    try:
        data = response.json()
    except Exception:
        data = {}

    return {
        "ok": response.status_code == 200,
        "status_code": response.status_code,
        "shop_name": data.get("shop", {}).get("name"),
        "domain": data.get("shop", {}).get("domain"),
        "myshopify_domain": data.get("shop", {}).get("myshopify_domain"),
        "errors": data.get("errors"),
        "token_prefix": token[:5],
        "dry_run": os.getenv("DRY_RUN", "true")
    }







@app.get("/dashboard/autopilot-history")
def dashboard_autopilot_history(limit: int = 50):
    from pathlib import Path
    import json

    log_dir = Path("app/logs/shopify_drafts")
    items = []

    if not log_dir.exists():
        return {"ok": True, "count": 0, "items": []}

    for file in sorted(log_dir.glob("*.json"), reverse=True)[:limit]:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            product = (
                data.get("result", {})
                .get("response", {})
                .get("product", {})
            )
            payload_product = data.get("payload", {}).get("product", {})
            variant = (product.get("variants") or payload_product.get("variants") or [{}])[0]

            items.append({
                "created_at": data.get("created_at"),
                "file": str(file),
                "product_id": product.get("id"),
                "title": product.get("title") or payload_product.get("title"),
                "sku": variant.get("sku"),
                "price": variant.get("price"),
                "status": product.get("status") or payload_product.get("status"),
                "created": data.get("result", {}).get("created"),
                "shopify_image": (product.get("image") or {}).get("src"),
                "source_image": ((payload_product.get("images") or [{}])[0]).get("src")
            })
        except Exception as e:
            items.append({
                "file": str(file),
                "error": str(e)
            })

    return {
        "ok": True,
        "count": len(items),
        "items": items
    }


@app.get("/dashboard/autopilot-schedule-status")
def dashboard_autopilot_schedule_status():
    import os

    return {
        "enabled": os.getenv("AUTOPILOT_SCHEDULE_ENABLED", "false"),
        "interval_hours": os.getenv("AUTOPILOT_INTERVAL_HOURS", "24"),
        "max_real_drafts": os.getenv("AUTOPILOT_MAX_REAL_DRAFTS", "3"),
        "min_score": os.getenv("AUTOPILOT_MIN_SCORE", "85"),
        "keywords": os.getenv("AUTOPILOT_KEYWORDS", "pet,travel pet,pet bowl"),
        "safety": {
            "shopify_status": "draft",
            "publishing": "disabled",
            "supplier_purchase": "disabled"
        }
    }


@app.on_event("startup")
async def start_autopilot_scheduler():
    import asyncio
    import os
    import json
    from pathlib import Path
    from datetime import datetime

    async def scheduler_loop():
        while True:
            try:
                enabled = os.getenv("AUTOPILOT_SCHEDULE_ENABLED", "false").lower() == "true"

                if enabled:
                    keywords = [
                        x.strip()
                        for x in os.getenv("AUTOPILOT_KEYWORDS", "pet,travel pet,pet bowl").split(",")
                        if x.strip()
                    ]

                    payload = {
                        "keywords": keywords,
                        "min_score": int(os.getenv("AUTOPILOT_MIN_SCORE", "85")),
                        "max_per_keyword": 3,
                        "max_real_drafts": int(os.getenv("AUTOPILOT_MAX_REAL_DRAFTS", "3"))
                    }

                    result = dashboard_autopilot_real_draft_run(payload)

                    log_dir = Path("app/logs/autopilot_scheduler")
                    log_dir.mkdir(parents=True, exist_ok=True)

                    log_file = log_dir / (datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json")
                    log_file.write_text(json.dumps({
                        "created_at": datetime.now().isoformat(),
                        "payload": payload,
                        "result": result
                    }, indent=2, ensure_ascii=False), encoding="utf-8")

                hours = int(os.getenv("AUTOPILOT_INTERVAL_HOURS", "24"))
                await asyncio.sleep(max(hours, 1) * 3600)

            except Exception as e:
                log_dir = Path("app/logs/autopilot_scheduler")
                log_dir.mkdir(parents=True, exist_ok=True)

                error_file = log_dir / "last_error.json"
                error_file.write_text(json.dumps({
                    "created_at": datetime.now().isoformat(),
                    "error": str(e)
                }, indent=2, ensure_ascii=False), encoding="utf-8")

                await asyncio.sleep(3600)

    asyncio.create_task(scheduler_loop())






@app.get("/dashboard/autopilot-kpis")
def dashboard_autopilot_kpis():
    from pathlib import Path
    import json

    log_dir = Path("app/logs/shopify_drafts")
    imported_file = Path("app/logs/imported_skus.json")

    total_logs = 0
    created_count = 0
    draft_count = 0
    active_count = 0
    estimated_revenue = 0.0
    products = []

    if log_dir.exists():
        for file in log_dir.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                total_logs += 1

                product = data.get("result", {}).get("response", {}).get("product", {})
                payload = data.get("payload", {}).get("product", {})
                variant = (product.get("variants") or payload.get("variants") or [{}])[0]

                created = bool(data.get("result", {}).get("created"))
                status = product.get("status") or payload.get("status")
                price = float(variant.get("price") or 0)

                if created:
                    created_count += 1
                    estimated_revenue += price

                if status == "active":
                    active_count += 1
                elif status == "draft":
                    draft_count += 1

                products.append({
                    "created_at": data.get("created_at"),
                    "product_id": product.get("id"),
                    "title": product.get("title") or payload.get("title"),
                    "sku": variant.get("sku"),
                    "price": price,
                    "status": status
                })

            except Exception:
                pass

    imported_skus = {}
    if imported_file.exists():
        try:
            imported_skus = json.loads(imported_file.read_text(encoding="utf-8"))
        except Exception:
            imported_skus = {}

    return {
        "ok": True,
        "total_logs": total_logs,
        "created_products": created_count,
        "draft_products": draft_count,
        "active_products": active_count,
        "tracked_skus": len(imported_skus),
        "estimated_revenue_if_one_each": round(estimated_revenue, 2),
        "publish_ratio_percent": round((active_count / created_count * 100), 2) if created_count else 0,
        "recent_products": sorted(products, key=lambda x: x.get("created_at") or "", reverse=True)[:10]
    }


@app.post("/dashboard/autopilot-schedule-update")
def dashboard_autopilot_schedule_update(payload: dict):
    from pathlib import Path
    import os

    env_file = Path(".env.local")
    text = env_file.read_text(encoding="utf-8") if env_file.exists() else ""

    updates = {
        "AUTOPILOT_SCHEDULE_ENABLED": str(payload.get("enabled", "false")).lower(),
        "AUTOPILOT_INTERVAL_HOURS": str(payload.get("interval_hours", 24)),
        "AUTOPILOT_MAX_REAL_DRAFTS": str(payload.get("max_real_drafts", 3)),
        "AUTOPILOT_MIN_SCORE": str(payload.get("min_score", 85)),
        "AUTOPILOT_KEYWORDS": ",".join(payload.get("keywords", [])) if isinstance(payload.get("keywords"), list) else str(payload.get("keywords", "pet,travel pet,pet bowl"))
    }

    for key, value in updates.items():
        if key in text:
            text = __import__("re").sub(rf"{key}=.*", f"{key}={value}", text)
        else:
            text += f"\n{key}={value}"

        os.environ[key] = value

    env_file.write_text(text, encoding="utf-8")

    return {
        "ok": True,
        "message": "Autopilot scheduler settings updated.",
        "settings": updates
    }


@app.get("/dashboard/autopilot-scheduler-last-run")
def dashboard_autopilot_scheduler_last_run():
    from pathlib import Path
    import json

    log_dir = Path("app/logs/autopilot_scheduler")

    if not log_dir.exists():
        return {"ok": True, "message": "No scheduler logs yet.", "last_run": None}

    files = sorted(log_dir.glob("*.json"), reverse=True)

    if not files:
        return {"ok": True, "message": "No scheduler logs yet.", "last_run": None}

    file = files[0]

    try:
        data = json.loads(file.read_text(encoding="utf-8"))
        return {
            "ok": True,
            "file": str(file),
            "last_run": data
        }
    except Exception as e:
        return {
            "ok": False,
            "file": str(file),
            "message": str(e)
        }


@app.get("/dashboard/shopify-products")
def dashboard_shopify_products(limit: int = 20):
    import os
    import requests

    store = os.getenv("SHOPIFY_STORE_URL", "").strip()
    store = store.replace("https://", "").replace("http://", "").rstrip("/")

    token = os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip()
    api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01")

    if not store or not token:
        return {
            "ok": False,
            "message": "Missing SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN",
            "products": []
        }

    response = requests.get(
        f"https://{store}/admin/api/{api_version}/products.json",
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        },
        params={"limit": max(1, min(limit, 50))},
        timeout=30
    )

    try:
        data = response.json()
    except Exception:
        data = {}

    products = []

    for p in data.get("products", []):
        variant = (p.get("variants") or [{}])[0]
        image = p.get("image") or {}

        products.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "status": p.get("status"),
            "published_at": p.get("published_at"),
            "price": variant.get("price"),
            "sku": variant.get("sku"),
            "inventory": variant.get("inventory_quantity"),
            "created_at": p.get("created_at"),
            "handle": p.get("handle"),
            "image": image.get("src")
        })

    return {
        "ok": response.status_code == 200,
        "status_code": response.status_code,
        "count": len(products),
        "products": products,
        "errors": data.get("errors")
    }


@app.get("/dashboard/shopify/live-check")
def dashboard_shopify_live_check():
    import os
    import requests

    store = (os.getenv("SHOPIFY_STORE_URL") or "").strip().replace("https://", "").replace("http://", "").rstrip("/")
    token = (os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "").strip()

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(
            f"https://{store}/admin/api/2024-01/shop.json",
            headers=headers,
            timeout=30
        )
        return {
            "ok": r.status_code == 200,
            "status_code": r.status_code,
            "store": store,
            "shop": r.json().get("shop") if r.status_code == 200 else None,
            "error": r.text[:1000] if r.status_code != 200 else None
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _shopify_find_product_by_sku(sku: str):
    import os
    import requests

    sku = (sku or "").strip()
    store = (os.getenv("SHOPIFY_STORE_URL") or "").strip().replace("https://", "").replace("http://", "").rstrip("/")
    token = (os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "").strip()

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    r = requests.get(
        f"https://{store}/admin/api/2024-01/products.json?limit=250",
        headers=headers,
        timeout=30
    )

    if r.status_code != 200:
        return {
            "ok": False,
            "status_code": r.status_code,
            "error": r.text[:1000]
        }

    for product in r.json().get("products", []):
        for variant in product.get("variants", []):
            if (variant.get("sku") or "").strip() == sku:
                return {
                    "ok": True,
                    "store": store,
                    "headers": headers,
                    "product": product,
                    "variant": variant
                }

    return {"ok": False, "message": f"SKU {sku} not found in Shopify"}


@app.post("/dashboard/shopify/product-live-details")
def dashboard_shopify_product_live_details(data: dict):
    sku = (data.get("sku") or "").strip()
    found = _shopify_find_product_by_sku(sku)

    if not found.get("ok"):
        return found

    product = found["product"]

    return {
        "ok": True,
        "product_id": product.get("id"),
        "title": product.get("title"),
        "status": product.get("status"),
        "published_at": product.get("published_at"),
        "variants": product.get("variants", []),
        "images": product.get("images", [])
    }


@app.post("/dashboard/shopify/update-inventory-live")
def dashboard_shopify_update_inventory_live(data: dict):
    import requests

    sku = (data.get("sku") or "").strip()
    quantity = int(data.get("quantity", 0))

    found = _shopify_find_product_by_sku(sku)

    if not found.get("ok"):
        return found

    store = found["store"]
    headers = found["headers"]
    product = found["product"]
    variant = found["variant"]
    inventory_item_id = variant.get("inventory_item_id")

    shop_response = requests.get(
        f"https://{store}/admin/api/2024-01/shop.json",
        headers=headers,
        timeout=30
    )

    if shop_response.status_code != 200:
        return {
            "ok": False,
            "status_code": shop_response.status_code,
            "error": shop_response.text[:1000]
        }

    location_id = shop_response.json().get("shop", {}).get("primary_location_id")

    inventory_response = requests.post(
        f"https://{store}/admin/api/2024-01/inventory_levels/set.json",
        headers=headers,
        json={
            "location_id": location_id,
            "inventory_item_id": inventory_item_id,
            "available": quantity
        },
        timeout=30
    )

    return {
        "ok": inventory_response.status_code in [200, 201],
        "mode": "shopify_inventory_update_by_sku_live",
        "status_code": inventory_response.status_code,
        "sku": sku,
        "quantity": quantity,
        "product_id": product.get("id"),
        "variant_id": variant.get("id"),
        "inventory_item_id": inventory_item_id,
        "location_id": location_id,
        "result": inventory_response.json() if inventory_response.text else None
    }


@app.get("/dashboard/shopify-products")
def dashboard_shopify_products():
    import os
    import requests

    store=(os.getenv("SHOPIFY_STORE_URL") or "").strip().replace("https://","").replace("http://","").rstrip("/")
    token=(os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "").strip()

    headers={
        "X-Shopify-Access-Token":token,
        "Content-Type":"application/json"
    }

    r=requests.get(
        f"https://{store}/admin/api/2024-01/products.json?limit=50",
        headers=headers,
        timeout=30
    )

    if r.status_code!=200:
        return {
            "ok":False,
            "status_code":r.status_code,
            "errors":r.text
        }

    products=r.json().get("products",[])

    return {
        "ok":True,
        "count":len(products),
        "products":products
    }


@app.post("/dashboard/shopify/sku-exists")
def dashboard_shopify_sku_exists(data: dict):

    sku=(data.get("sku") or "").strip()

    found=_shopify_find_product_by_sku(sku)

    if not found.get("ok"):
        return {
            "exists":False,
            "sku":sku
        }

    product=found["product"]
    variant=found["variant"]

    return {
        "exists":True,
        "sku":sku,
        "product_id":product.get("id"),
        "title":product.get("title"),
        "status":product.get("status"),
        "variant_id":variant.get("id")
    }


@app.post("/dashboard/shopify/delete-product")
def dashboard_shopify_delete_product(data: dict):
    import os
    import requests

    product_id = str(data.get("product_id","")).strip()

    store=(os.getenv("SHOPIFY_STORE_URL") or "").strip().replace("https://","").replace("http://","").rstrip("/")
    token=(os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "").strip()

    r=requests.delete(
        f"https://{store}/admin/api/2024-01/products/{product_id}.json",
        headers={
            "X-Shopify-Access-Token":token
        },
        timeout=30
    )

    return {
        "ok": r.status_code in [200,202],
        "status_code": r.status_code,
        "product_id": product_id,
        "response": r.text[:500]
    }


@app.post("/dashboard/shopify/safe-create-or-update")
def dashboard_shopify_safe_create_or_update(payload: dict):
    sku = (payload.get("sku") or payload.get("pid") or "").strip()

    if not sku:
        return {
            "ok": False,
            "message": "Missing SKU"
        }

    duplicate = _shopify_find_product_by_sku(sku)

    if duplicate.get("ok"):
        product = duplicate["product"]
        variant = duplicate["variant"]

        return {
            "ok": True,
            "mode": "duplicate_blocked_existing_product_returned",
            "created": False,
            "updated": False,
            "sku": sku,
            "product_id": product.get("id"),
            "variant_id": variant.get("id"),
            "title": product.get("title"),
            "status": product.get("status")
        }

    return dashboard_shopify_draft_from_ai(payload)


@app.get("/dashboard/shopify/catalog-health")
def dashboard_shopify_catalog_health():
    products_response = dashboard_shopify_products()

    if not products_response.get("ok"):
        return products_response

    products = products_response.get("products", [])

    active = [p for p in products if p.get("status") == "active"]
    draft = [p for p in products if p.get("status") == "draft"]

    sku_counts = {}
    for p in products:
        sku=""

        variants=p.get("variants",[])

        if variants:
            sku=(variants[0].get("sku") or "").strip()
        if sku:
            sku_counts[sku] = sku_counts.get(sku, 0) + 1

    duplicate_skus = {
        sku: count
        for sku, count in sku_counts.items()
        if count > 1
    }

    return {
        "ok": True,
        "total_products": len(products),
        "active_products": len(active),
        "draft_products": len(draft),
        "duplicate_sku_count": len(duplicate_skus),
        "duplicate_skus": duplicate_skus,
        "health": "ok" if len(duplicate_skus) == 0 else "needs_cleanup"
    }




app.include_router(commerce_router)


