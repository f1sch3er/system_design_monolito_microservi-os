import uuid
from typing import Any, Dict, List, Optional


class Store:
    def __init__(self) -> None:
        self._items: Dict[str, Dict[str, Any]] = {}

    def next_id(self) -> str:
        return uuid.uuid4().hex

    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        self._items[item["id"]] = item
        return item

    def get(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self._items.get(item_id)

    def all(self) -> List[Dict[str, Any]]:
        return list(self._items.values())

    def count(self) -> int:
        return len(self._items)

    def update(self, item_id: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if item_id not in self._items:
            return None
        self._items[item_id] = item
        return item

    def delete(self, item_id: str) -> bool:
        return self._items.pop(item_id, None) is not None


users_store = Store()
