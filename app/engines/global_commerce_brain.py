from datetime import datetime


class GlobalCommerceBrain:
    def __init__(self):
        self.name = "global_commerce_brain"
        self.version = "0.4.0"

    def choose_best_available_channels(self) -> list:
        from app.engines.marketplace_scoring import get_best_marketplaces

        supported_channels = ["shopify", "woocommerce", "meta_shop"]
        ranked = get_best_marketplaces(limit=20).get("marketplaces", [])

        selected = [
            item["channel"]
            for item in ranked
            if item.get("channel") in supported_channels
        ]

        return selected or ["shopify"]

    def choose_actions(self, sku: str, rule: str, data: dict) -> dict:
        actions = []
        channels = data.get("channels") or self.choose_best_available_channels()

        if rule == "auto_restock":
            actions.append({
                "action": "update_inventory",
                "quantity": int(data.get("restock_to", 50)),
                "amount": float(data.get("spend_amount", 0)),
                "reason": "auto_restock"
            })

        elif rule == "price_margin_guard":
            cost = float(data.get("cost", 0))
            shipping_cost = float(data.get("shipping_cost", 0))
            min_margin_percent = float(data.get("min_margin_percent", 30))

            if min_margin_percent >= 100:
                return {"ok": False, "message": "min_margin_percent must be below 100"}

            minimum_price = round(
                (cost + shipping_cost) / (1 - (min_margin_percent / 100)),
                2
            )

            actions.append({
                "action": "update_price",
                "price": minimum_price,
                "amount": 0,
                "reason": "price_margin_guard",
                "cost": cost,
                "shipping_cost": shipping_cost,
                "min_margin_percent": min_margin_percent
            })

        elif rule == "archive":
            actions.append({
                "action": "archive",
                "amount": 0,
                "reason": data.get("reason", "brain_archive")
            })

        elif rule == "publish_missing":
            actions.append({
                "action": "publish_missing",
                "amount": float(data.get("spend_amount", 0)),
                "reason": "cross_channel_publish_missing"
            })

        else:
            return {
                "ok": False,
                "message": f"Unsupported brain rule: {rule}",
                "supported_rules": [
                    "auto_restock",
                    "price_margin_guard",
                    "archive",
                    "publish_missing"
                ]
            }

        return {
            "ok": True,
            "sku": sku,
            "channels": channels,
            "rule": rule,
            "actions": actions,
            "decided_at": datetime.now().isoformat()
        }

    def channel_has_sku(self, channel: str, sku: str) -> dict:
        from app.channels.channel_manager import run_channel_action

        try:
            result = run_channel_action(
                channel=channel,
                action="get_details",
                payload={"sku": sku}
            )

            return {
                "ok": True,
                "exists": result.get("ok") is True,
                "channel": channel,
                "sku": sku,
                "details": result
            }

        except Exception as e:
            return {
                "ok": False,
                "exists": False,
                "channel": channel,
                "sku": sku,
                "error": str(e)
            }

    def extract_product_for_publish(self, source_presence: dict) -> dict:
        details = source_presence.get("details", {})

        if "product" in details:
            p = details.get("product", {})
            return {
                "sku": p.get("sku"),
                "title": p.get("name") or p.get("title"),
                "name": p.get("name") or p.get("title"),
                "price": p.get("price") or p.get("regular_price") or 0,
                "inventory": p.get("stock_quantity") or 0,
                "description": p.get("description") or p.get("short_description") or "",
                "status": "draft"
            }

        if "title" in details:
            variants = details.get("variants", [])
            variant = variants[0] if variants else {}

            return {
                "sku": variant.get("sku"),
                "title": details.get("title"),
                "name": details.get("title"),
                "price": variant.get("price") or 0,
                "inventory": variant.get("inventory_quantity") or 0,
                "description": details.get("title"),
                "status": "draft"
            }

        return {}

    def financial_gate(self, sku: str, channel: str, action: dict) -> dict:
        from app.engines.risk_guard import check_risk
        from app.engines.wallet_engine import can_spend, reserve

        amount = float(action.get("amount", 0) or 0)

        risk = check_risk({
            "sku": sku,
            "channel": channel,
            "action": action.get("action"),
            "amount": amount,
            "reason": action.get("reason")
        })

        if not risk.get("allowed"):
            return {
                "ok": False,
                "stage": "risk_guard",
                "risk": risk
            }

        wallet_check = can_spend(
            amount=amount,
            reason=action.get("reason")
        )

        if not wallet_check.get("allowed"):
            return {
                "ok": False,
                "stage": "wallet_check",
                "wallet_check": wallet_check
            }

        reservation = reserve(
            amount=amount,
            reason=action.get("reason"),
            metadata={
                "sku": sku,
                "channel": channel,
                "action": action
            }
        )

        if not reservation.get("ok"):
            return {
                "ok": False,
                "stage": "wallet_reserve",
                "reservation": reservation
            }

        return {
            "ok": True,
            "amount": amount,
            "risk": risk,
            "wallet_check": wallet_check,
            "reservation": reservation
        }

    def execute_actions(self, sku: str, channels: list, actions: list) -> dict:
        from app.channels.channel_manager import run_channel_action
        from app.engines.wallet_engine import spend, release

        results = []

        for channel in channels:
            presence = self.channel_has_sku(channel, sku)

            if not presence.get("exists"):
                source_presence = None

                for source_channel in channels:
                    if source_channel == channel:
                        continue

                    source_check = self.channel_has_sku(source_channel, sku)

                    if source_check.get("exists"):
                        source_presence = source_check
                        break

                for action in actions:
                    if action.get("action") == "publish_missing" and source_presence:
                        product_payload = self.extract_product_for_publish(source_presence)

                        try:
                            publish_result = run_channel_action(
                                channel=channel,
                                action="publish_product",
                                payload=product_payload
                            )
                        except Exception as e:
                            publish_result = {"ok": False, "error": str(e)}

                        results.append({
                            "channel": channel,
                            "action": "publish_product",
                            "cross_channel_publish": True,
                            "source_channel": source_presence.get("channel"),
                            "target_channel": channel,
                            "product_payload": product_payload,
                            "result": publish_result
                        })

                    else:
                        results.append({
                            "channel": channel,
                            "action": action.get("action"),
                            "skipped": True,
                            "skip_reason": "sku_not_found_on_channel",
                            "presence": presence,
                            "result": {
                                "ok": True,
                                "skipped": True,
                                "message": "SKU not found on this channel, action skipped"
                            }
                        })

                continue

            for action in actions:
                if action.get("action") == "publish_missing":
                    results.append({
                        "channel": channel,
                        "action": action.get("action"),
                        "skipped": True,
                        "skip_reason": "sku_already_exists_on_channel",
                        "presence": presence,
                        "result": {
                            "ok": True,
                            "skipped": True,
                            "message": "SKU already exists on this channel"
                        }
                    })
                    continue

                gate = self.financial_gate(
                    sku=sku,
                    channel=channel,
                    action=action
                )

                if not gate.get("ok"):
                    results.append({
                        "channel": channel,
                        "action": action.get("action"),
                        "financial_gate": gate,
                        "result": {
                            "ok": False,
                            "message": "financial gate blocked action"
                        }
                    })
                    continue

                payload = {
                    "sku": sku,
                    **action
                }

                try:
                    result = run_channel_action(
                        channel=channel,
                        action=action.get("action"),
                        payload=payload
                    )
                except Exception as e:
                    result = {
                        "ok": False,
                        "channel": channel,
                        "action": action.get("action"),
                        "error": str(e)
                    }

                amount = float(action.get("amount", 0) or 0)

                if result.get("ok"):
                    wallet_result = spend(
                        amount=amount,
                        reason=action.get("reason"),
                        metadata={
                            "sku": sku,
                            "channel": channel,
                            "action": action,
                            "result": result
                        }
                    )
                else:
                    wallet_result = release(
                        amount=amount,
                        reason="release_after_failed_action",
                        metadata={
                            "sku": sku,
                            "channel": channel,
                            "action": action,
                            "result": result
                        }
                    )

                results.append({
                    "channel": channel,
                    "action": action.get("action"),
                    "financial_gate": gate,
                    "result": result,
                    "wallet_result": wallet_result
                })

        return {
            "ok": all(r.get("result", {}).get("ok") for r in results),
            "sku": sku,
            "executed_at": datetime.now().isoformat(),
            "results": results
        }

    def run(self, data: dict) -> dict:
        sku = data.get("sku")
        rule = data.get("rule")
        channels = data.get("channels") or self.choose_best_available_channels()

        if not sku:
            return {"ok": False, "message": "missing sku"}

        if not rule:
            return {"ok": False, "message": "missing rule"}

        decision = self.choose_actions(
            sku=sku,
            rule=rule,
            data={
                **data,
                "channels": channels
            }
        )

        if not decision.get("ok"):
            return decision

        execution = self.execute_actions(
            sku=sku,
            channels=channels,
            actions=decision.get("actions", [])
        )

        result = {
            "ok": execution.get("ok"),
            "mode": "global_commerce_brain",
            "brain_version": self.version,
            "sku": sku,
            "channels": channels,
            "rule": rule,
            "decision": decision,
            "execution": execution
        }

        try:
            from app.engines.decision_memory import record_decision
            result["memory"] = record_decision(result)
        except Exception as e:
            result["memory"] = {
                "ok": False,
                "error": str(e)
            }

        return result


def run_global_commerce_brain(data: dict) -> dict:
    brain = GlobalCommerceBrain()
    return brain.run(data)


def brain_status() -> dict:
    brain = GlobalCommerceBrain()

    return {
        "ok": True,
        "mode": brain.name,
        "version": brain.version,
        "supported_rules": [
            "auto_restock",
            "price_margin_guard",
            "archive",
            "publish_missing"
        ],
        "financial_gate": [
            "risk_guard",
            "wallet_engine"
        ],
        "status": "ready"
    }

