from models import MenuItem

_items: dict[int, MenuItem] = {}
_by_key: dict[str, int] = {}
_next_id = 1

def create(restaurant_id: int, name: str, price_paise: int, key: str | None = None) -> MenuItem:
    global _next_id
    item = MenuItem(
        id=_next_id,
        restaurant_id=restaurant_id,
        name=name,
        price_paise=price_paise,
        internal_sku=f"SKU-{_next_id}",
        idempotency_key=key
    )
    _items[item.id] = item
    if key:
        _by_key[key] = item.id
    _next_id += 1
    return item

def find(item_id: int) -> MenuItem | None:
    return _items.get(item_id)

def find_by_key(key: str) -> MenuItem | None:
    item_id = _by_key.get(key)
    return _items.get(item_id) if item_id else None

def find_by_restaurant(restaurant_id: int) -> list[MenuItem]:
    return [i for i in _items.values() if i.restaurant_id == restaurant_id]