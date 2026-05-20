from app.support.schemas import SupportRequest, SupportMessage, SupportContext
from app.support.service import CustomerSupportAI
from app.support.schemas import SupportIntent, EscalationReason
from app.fulfillment.schemas import FulfillmentResult, FulfillmentStatus


def test_support_classifies_tracking_message():
    ai = CustomerSupportAI()
    req = SupportRequest(message=SupportMessage(order_id="ORD-1", customer_message="Where is my tracking number?"))
    result = ai.classify(req)
    assert result.intent == SupportIntent.TRACKING
    assert result.confidence >= 0.55
    assert result.escalate is False


def test_support_escalates_legal_threat():
    ai = CustomerSupportAI()
    req = SupportRequest(message=SupportMessage(order_id="ORD-2", customer_message="I will call my lawyer and sue you"))
    result = ai.classify(req)
    assert result.escalate is True
    assert EscalationReason.LEGAL_THREAT in result.escalation_reasons


def test_support_reply_auto_send_blocked_when_escalated():
    ai = CustomerSupportAI()
    req = SupportRequest(
        message=SupportMessage(order_id="ORD-3", customer_message="This is a scam and I will do a chargeback"),
        auto_send_allowed=True,
    )
    reply = ai.draft_reply(req)
    assert reply.escalate is True
    assert reply.auto_send_allowed is False
    assert "route_to_human_review" in reply.next_actions


def test_support_reply_includes_tracking_from_fulfillment_context():
    ai = CustomerSupportAI()
    fulfillment = FulfillmentResult(
        status=FulfillmentStatus.PURCHASED,
        order_id="ORD-4",
        supplier_id="mock",
        supplier_product_id="P1",
        supplier_order_id="SO-1",
        tracking_number="TRACK123",
    )
    req = SupportRequest(
        message=SupportMessage(order_id="ORD-4", customer_message="Can I track my package?", customer_name="Alex"),
        context=SupportContext(fulfillment=fulfillment, store_name="Test Store"),
        auto_send_allowed=True,
    )
    reply = ai.draft_reply(req)
    assert reply.intent == SupportIntent.TRACKING
    assert reply.auto_send_allowed is True
    assert "TRACK123" in reply.body
    assert "Test Store" in reply.body


def test_support_high_value_order_escalates():
    ai = CustomerSupportAI()
    req = SupportRequest(
        message=SupportMessage(order_id="ORD-5", customer_message="Where is my delivery?"),
        context=SupportContext(order_value=400),
    )
    result = ai.classify(req)
    assert result.escalate is True
    assert EscalationReason.HIGH_VALUE_ORDER in result.escalation_reasons
