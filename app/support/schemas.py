from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, field_validator

from app.shipping.schemas import TrackingEvent
from app.fulfillment.schemas import FulfillmentResult


class SupportIntent(str, Enum):
    TRACKING = "tracking"
    RETURN_REQUEST = "return_request"
    CANCELLATION = "cancellation"
    DAMAGED_ITEM = "damaged_item"
    REFUND_STATUS = "refund_status"
    PRODUCT_QUESTION = "product_question"
    ADDRESS_CHANGE = "address_change"
    COMPLAINT = "complaint"
    UNKNOWN = "unknown"


class SupportTone(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CONCISE = "concise"


class EscalationReason(str, Enum):
    LEGAL_THREAT = "legal_threat"
    CHARGEBACK_OR_FRAUD = "chargeback_or_fraud"
    HIGH_VALUE_ORDER = "high_value_order"
    POLICY_EXCEPTION = "policy_exception"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    UNKNOWN_INTENT = "unknown_intent"


class SupportMessage(BaseModel):
    order_id: str | None = Field(default=None, min_length=1)
    customer_message: str = Field(min_length=2, max_length=4000)
    customer_name: str | None = Field(default=None, max_length=120)
    language: str = Field(default="en", min_length=2, max_length=8)

    @field_validator("language")
    @classmethod
    def normalize_language(cls, value: str) -> str:
        return value.lower()


class SupportContext(BaseModel):
    fulfillment: FulfillmentResult | None = None
    tracking_events: list[TrackingEvent] = Field(default_factory=list)
    order_value: float | None = Field(default=None, ge=0)
    return_window_days: int = Field(default=30, ge=0, le=365)
    marketplace_policy_url: str | None = None
    store_name: str = "our store"


class SupportRequest(BaseModel):
    message: SupportMessage
    context: SupportContext = Field(default_factory=SupportContext)
    tone: SupportTone = SupportTone.PROFESSIONAL
    auto_send_allowed: bool = False


class SupportClassification(BaseModel):
    intent: SupportIntent
    confidence: float = Field(ge=0, le=1)
    sentiment_score: float = Field(ge=-1, le=1)
    escalate: bool
    escalation_reasons: list[EscalationReason] = Field(default_factory=list)
    detected_keywords: list[str] = Field(default_factory=list)


class SupportReply(BaseModel):
    intent: SupportIntent
    confidence: float = Field(ge=0, le=1)
    escalate: bool
    auto_send_allowed: bool
    subject: str
    body: str
    next_actions: list[str] = Field(default_factory=list)
    audit_events: list[str] = Field(default_factory=list)
