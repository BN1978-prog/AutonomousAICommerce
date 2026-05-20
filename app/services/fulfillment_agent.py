class FulfillmentAgent:
    def create_supplier_order(self, order: dict) -> dict:
        # Replace with approved supplier API integration.
        return {
            "status": "SIMULATED",
            "supplier_order_id": "SIM-ORDER-001",
            "tracking_number": "SIM-TRACK-001",
            "note": "No real purchase was made. Connect supplier API before production use.",
            "order": order,
        }
