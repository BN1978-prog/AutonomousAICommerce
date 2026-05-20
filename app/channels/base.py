from abc import ABC, abstractmethod


class BaseChannelAdapter(ABC):
    channel_name = "base"

    def capabilities(self) -> dict:
        return {
            "create_draft": False,
            "publish": False,
            "update_price": False,
            "update_inventory": False,
            "disable_product": False,
            "read_orders": False,
            "read_performance": False
        }

    @abstractmethod
    def status(self) -> dict:
        pass

    @abstractmethod
    def validate_product(self, product: dict) -> dict:
        pass

    @abstractmethod
    def create_draft(self, product: dict) -> dict:
        pass

    @abstractmethod
    def publish(self, product_id: str) -> dict:
        pass

    @abstractmethod
    def update_price(self, sku: str, price: float) -> dict:
        pass

    @abstractmethod
    def disable_product(self, product_id: str) -> dict:
        pass

    def execute_publish_preview(self, job: dict) -> dict:
        return {
            "ok": False,
            "status": "failed_preview",
            "channel": self.channel_name,
            "message": f"{self.channel_name} preview executor not implemented"
        }

