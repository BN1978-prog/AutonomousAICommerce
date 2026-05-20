from __future__ import annotations

from datetime import UTC, datetime

from app.support.schemas import (
    EscalationReason,
    SupportClassification,
    SupportIntent,
    SupportReply,
    SupportRequest,
    SupportTone,
)


class CustomerSupportAI:
    """Deterministic, policy-safe support assistant.

    The first production version intentionally avoids free-form uncontrolled LLM
    output. It classifies common ecommerce requests and creates bounded replies
    from templates. An LLM can be added later behind the same interface.
    """

    _INTENT_KEYWORDS: dict[SupportIntent, tuple[str, ...]] = {
        SupportIntent.TRACKING: ("where", "tracking", "track", "delivered", "delivery", "arrive", "parcel", "package"),
        SupportIntent.RETURN_REQUEST: ("return", "send back", "exchange", "not suitable"),
        SupportIntent.CANCELLATION: ("cancel", "cancellation", "stop order"),
        SupportIntent.DAMAGED_ITEM: ("damaged", "broken", "faulty", "defective", "not working"),
        SupportIntent.REFUND_STATUS: ("refund", "money back", "reimbursed"),
        SupportIntent.ADDRESS_CHANGE: ("address", "wrong address", "change address"),
        SupportIntent.PRODUCT_QUESTION: ("size", "colour", "color", "compatible", "material", "dimension"),
        SupportIntent.COMPLAINT: ("angry", "complaint", "unhappy", "terrible", "bad service", "scam"),
    }

    _ESCALATION_KEYWORDS: dict[EscalationReason, tuple[str, ...]] = {
        EscalationReason.LEGAL_THREAT: ("lawyer", "solicitor", "court", "legal", "sue"),
        EscalationReason.CHARGEBACK_OR_FRAUD: ("chargeback", "fraud", "unauthorized", "unauthorised", "stolen card"),
        EscalationReason.POLICY_EXCEPTION: ("exception", "outside policy", "after 30 days"),
    }

    def classify(self, request: SupportRequest) -> SupportClassification:
        text = request.message.customer_message.lower()
        best_intent = SupportIntent.UNKNOWN
        best_hits: list[str] = []

        for intent, keywords in self._INTENT_KEYWORDS.items():
            hits = [kw for kw in keywords if kw in text]
            if len(hits) > len(best_hits):
                best_intent = intent
                best_hits = hits

        confidence = min(0.95, 0.35 + (len(best_hits) * 0.18)) if best_hits else 0.25
        sentiment_score = self._sentiment_score(text)
        reasons: list[EscalationReason] = []

        for reason, keywords in self._ESCALATION_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                reasons.append(reason)

        if request.context.order_value is not None and request.context.order_value >= 250:
            reasons.append(EscalationReason.HIGH_VALUE_ORDER)
        if sentiment_score <= -0.55:
            reasons.append(EscalationReason.NEGATIVE_SENTIMENT)
        if best_intent == SupportIntent.UNKNOWN:
            reasons.append(EscalationReason.UNKNOWN_INTENT)

        return SupportClassification(
            intent=best_intent,
            confidence=confidence,
            sentiment_score=sentiment_score,
            escalate=bool(reasons),
            escalation_reasons=list(dict.fromkeys(reasons)),
            detected_keywords=best_hits,
        )

    def draft_reply(self, request: SupportRequest) -> SupportReply:
        classification = self.classify(request)
        greeting = self._greeting(request)
        signoff = f"\n\nKind regards,\n{request.context.store_name} Support"
        subject = self._subject(classification.intent)
        body = self._body_for_intent(classification.intent, request, greeting) + signoff
        next_actions = self._next_actions(classification.intent, classification.escalate)
        auto_send_allowed = request.auto_send_allowed and not classification.escalate and classification.confidence >= 0.55
        audit_events = [
            f"{datetime.now(UTC).isoformat()} classified_intent={classification.intent.value}",
            f"{datetime.now(UTC).isoformat()} escalate={classification.escalate}",
            f"{datetime.now(UTC).isoformat()} auto_send_allowed={auto_send_allowed}",
        ]
        return SupportReply(
            intent=classification.intent,
            confidence=classification.confidence,
            escalate=classification.escalate,
            auto_send_allowed=auto_send_allowed,
            subject=subject,
            body=body,
            next_actions=next_actions,
            audit_events=audit_events,
        )

    def _sentiment_score(self, text: str) -> float:
        negative = ("angry", "terrible", "awful", "scam", "bad", "unhappy", "disappointed", "complaint")
        positive = ("thanks", "thank you", "great", "happy", "perfect")
        score = 0.0
        score -= sum(0.18 for word in negative if word in text)
        score += sum(0.12 for word in positive if word in text)
        return max(-1.0, min(1.0, score))

    def _greeting(self, request: SupportRequest) -> str:
        name = request.message.customer_name
        if request.tone == SupportTone.CONCISE:
            return "Hello," if not name else f"Hello {name},"
        return "Hi," if not name else f"Hi {name},"

    def _subject(self, intent: SupportIntent) -> str:
        mapping = {
            SupportIntent.TRACKING: "Update on your order",
            SupportIntent.RETURN_REQUEST: "Return request received",
            SupportIntent.CANCELLATION: "Cancellation request received",
            SupportIntent.DAMAGED_ITEM: "Help with your item",
            SupportIntent.REFUND_STATUS: "Refund status update",
            SupportIntent.PRODUCT_QUESTION: "Product question",
            SupportIntent.ADDRESS_CHANGE: "Address change request",
            SupportIntent.COMPLAINT: "We are reviewing your message",
            SupportIntent.UNKNOWN: "We are reviewing your message",
        }
        return mapping[intent]

    def _body_for_intent(self, intent: SupportIntent, request: SupportRequest, greeting: str) -> str:
        order_line = f" for order {request.message.order_id}" if request.message.order_id else ""
        latest_event = request.context.tracking_events[-1] if request.context.tracking_events else None
        tracking = request.context.fulfillment.tracking_number if request.context.fulfillment else None

        if intent == SupportIntent.TRACKING:
            if latest_event:
                return (
                    f"{greeting}\n\nThanks for your message{order_line}. The latest tracking update is: "
                    f"{latest_event.status} in {latest_event.location}. {latest_event.message}"
                )
            if tracking:
                return f"{greeting}\n\nThanks for your message{order_line}. Your tracking number is {tracking}."
            return f"{greeting}\n\nThanks for your message{order_line}. We are checking the tracking details and will update you shortly."

        if intent == SupportIntent.RETURN_REQUEST:
            return (
                f"{greeting}\n\nThanks for contacting us{order_line}. Returns are reviewed against the "
                f"{request.context.return_window_days}-day return window. Please keep the item unused and in its original packaging while we review this."
            )

        if intent == SupportIntent.CANCELLATION:
            return f"{greeting}\n\nThanks for contacting us{order_line}. We will check whether the order can still be cancelled before dispatch."

        if intent == SupportIntent.DAMAGED_ITEM:
            return f"{greeting}\n\nI am sorry to hear there is an issue{order_line}. Please send a clear photo of the item and packaging so we can review the best solution."

        if intent == SupportIntent.REFUND_STATUS:
            return f"{greeting}\n\nThanks for your message{order_line}. We are checking the refund status and will update you with the latest information."

        if intent == SupportIntent.ADDRESS_CHANGE:
            return f"{greeting}\n\nThanks for the update{order_line}. We will check whether the address can still be changed before dispatch."

        if intent == SupportIntent.PRODUCT_QUESTION:
            return f"{greeting}\n\nThanks for your question. We are checking the product details and will reply with the most accurate information."

        return f"{greeting}\n\nThanks for your message{order_line}. We are reviewing this and will respond with the next step."

    def _next_actions(self, intent: SupportIntent, escalate: bool) -> list[str]:
        if escalate:
            return ["route_to_human_review", "pause_auto_send"]
        mapping = {
            SupportIntent.TRACKING: ["send_tracking_update"],
            SupportIntent.RETURN_REQUEST: ["check_return_window", "prepare_return_instructions"],
            SupportIntent.CANCELLATION: ["check_dispatch_status"],
            SupportIntent.DAMAGED_ITEM: ["request_photos", "review_supplier_policy"],
            SupportIntent.REFUND_STATUS: ["check_payment_gateway"],
            SupportIntent.ADDRESS_CHANGE: ["check_dispatch_status", "update_address_if_safe"],
            SupportIntent.PRODUCT_QUESTION: ["fetch_product_specs"],
            SupportIntent.COMPLAINT: ["route_to_human_review"],
            SupportIntent.UNKNOWN: ["route_to_human_review"],
        }
        return mapping[intent]
