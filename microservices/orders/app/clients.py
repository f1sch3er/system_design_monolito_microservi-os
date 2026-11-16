import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger("orders.clients")

API_KEY = os.getenv("API_KEY", "dev-api-key")
USERS_URL = os.getenv("USERS_URL", "http://localhost:8002")
PRODUCTS_URL = os.getenv("PRODUCTS_URL", "http://localhost:8001")


def get_user(user_id: str) -> Optional[dict]:
    resp = httpx.get(f"{USERS_URL}/users/{user_id}", headers={"X-API-Key": API_KEY})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def get_product(product_id: str) -> Optional[dict]:
    resp = httpx.get(f"{PRODUCTS_URL}/products/{product_id}", headers={"X-API-Key": API_KEY})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()
