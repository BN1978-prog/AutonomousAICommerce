import os
from dataclasses import dataclass

@dataclass
class RiskDecision:
    allowed: bool
    reason: str

def env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default

def is_emergency_stop() -> bool:
    return os.getenv("EMERGENCY_STOP", "false").lower() == "true"

def check_trade_allowed(estimated_spend: float, margin_percent: float) -> RiskDecision:
    if is_emergency_stop():
        return RiskDecision(False, "Emergency stop is enabled.")

    max_daily_spend = env_float("MAX_DAILY_SPEND", 250)
    min_margin = env_float("MIN_MARGIN_PERCENT", 25)

    if estimated_spend > max_daily_spend:
        return RiskDecision(False, f"Estimated spend {estimated_spend} exceeds max daily spend {max_daily_spend}.")

    if margin_percent < min_margin:
        return RiskDecision(False, f"Margin {margin_percent}% is below minimum {min_margin}%.")

    if os.getenv("DRY_RUN", "true").lower() == "true":
        return RiskDecision(True, "Allowed in dry-run mode only.")

    if os.getenv("AUTONOMY_ENABLED", "false").lower() != "true":
        return RiskDecision(False, "Autonomy is disabled.")

    return RiskDecision(True, "Trade allowed.")
