from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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




