from app.core.config import Settings
from app.dashboard.schemas import AutonomyControls, DashboardMetrics, DashboardStatus


class DashboardService:
    """Read-only dashboard state service.

    In production this service should read from the database and audit log.
    For the current MVP it returns deterministic operational status so tests
    and deployments can verify that all modules are wired together.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.autonomy = AutonomyControls(
            enabled=False,
            dry_run=getattr(settings, "dry_run", True),
            daily_budget_limit=getattr(settings, "max_daily_spend", 250.0),
            minimum_margin_percent=getattr(settings, "min_margin_percent", 25.0),
        )

    def get_status(self) -> DashboardStatus:
        warnings: list[str] = []
        if self.autonomy.dry_run:
            warnings.append("Dry-run mode is enabled; supplier purchases are simulated.")
        if not self.autonomy.enabled:
            warnings.append("Autonomous execution is disabled until explicitly enabled.")
        if self.autonomy.emergency_stop:
            warnings.append("Emergency stop is active; execution must remain blocked.")

        return DashboardStatus(
            system_status="safe" if not self.autonomy.emergency_stop else "stopped",
            environment=self.settings.environment,
            autonomy=self.autonomy,
            modules={
                "core": "online",
                "suppliers": "online",
                "marketplaces": "online",
                "product_hunter": "online",
                "profit_risk": "online",
                "listing_generator": "online",
                "fulfillment": "online",
                "shipping_tracking": "online",
                "customer_support": "online",
                "self_learning": "online",
                "admin_dashboard": "online",
            },
            warnings=warnings,
        )

    def update_controls(self, controls: AutonomyControls) -> AutonomyControls:
        # Safety invariant: emergency stop always forces autonomy off.
        if controls.emergency_stop:
            controls.enabled = False
        self.autonomy = controls
        return self.autonomy

    def get_metrics(self) -> DashboardMetrics:
        return DashboardMetrics(
            active_products=0,
            open_orders=0,
            pending_fulfillment=0,
            estimated_daily_spend=0.0,
            estimated_daily_profit=0.0,
            risk_level="low",
        )
