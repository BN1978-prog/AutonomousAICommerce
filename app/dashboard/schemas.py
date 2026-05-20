from pydantic import BaseModel, Field


class AutonomyControls(BaseModel):
    enabled: bool = Field(default=False, description="Whether autonomous execution is enabled")
    dry_run: bool = Field(default=True, description="When true, no real supplier purchase is performed")
    daily_budget_limit: float = Field(default=250.0, ge=0)
    max_orders_per_day: int = Field(default=10, ge=0)
    minimum_margin_percent: float = Field(default=25.0, ge=0)
    emergency_stop: bool = Field(default=False)


class DashboardStatus(BaseModel):
    system_status: str
    environment: str
    autonomy: AutonomyControls
    modules: dict[str, str]
    warnings: list[str]


class DashboardMetrics(BaseModel):
    active_products: int
    open_orders: int
    pending_fulfillment: int
    estimated_daily_spend: float
    estimated_daily_profit: float
    risk_level: str
