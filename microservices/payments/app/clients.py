import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger("payments.clients")

API_KEY = os.getenv("API_KEY", "dev-api-key")
ORDERS_URL = os.getenv("ORDERS_URL", "http://localhost:8003")


def get_order(order_id: str) -> Optional[dict]:
    resp = httpx.get(f"{ORDERS_URL}/orders/{order_id}", headers={"X-API-Key": API_KEY})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def mark_order_paid(order_id: str) -> None:
    resp = httpx.post(f"{ORDERS_URL}/orders/{order_id}/mark-paid", headers={"X-API-Key": API_KEY})
    resp.raise_for_status()
