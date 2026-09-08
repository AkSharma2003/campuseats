from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class MenuItem:
    id: int
    restaurant_id: int
    name: str
    price_paise: int
    is_available: bool = True
    internal_sku: str = ""  # Internal field; representation me leak nahi hoga
    idempotency_key: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def as_json(self) -> dict:
        """API Response formatting"""
        return {
            "id": self.id,
            "restaurantId": self.restaurant_id,
            "name": self.name,
            "pricePaise": self.price_paise,
            "isAvailable": self.is_available,
            "createdAt": self.created_at.isoformat()
        }