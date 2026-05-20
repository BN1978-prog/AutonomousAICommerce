from __future__ import annotations

from pydantic import BaseModel, Field


class RiskSignal(BaseModel):
    name: str
    score: float = Field(ge=0, le=1)
    weight: float = Field(ge=0, le=1)
    explanation: str


class AdvancedRiskReport(BaseModel):
    total_score: float = Field(ge=0, le=1)
    level: str
    signals: list[RiskSignal]
    blocking_reasons: list[str]
    watch_reasons: list[str]
