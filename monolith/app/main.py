import logging
import os

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .routers import orders, payments, products, users
from .storage import orders_store, payments_store, products_store, users_store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="E-commerce - Monolito")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response


app.add_middleware(SecurityHeadersMiddleware)

allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


@app.get("/health")
def health():
    modules = {
        "products": products_store.count(),
        "users": users_store.count(),
        "orders": orders_store.count(),
        "payments": payments_store.count(),
    }
    return {
        "status": "ok",
        "modules": {name: {"ok": True, "records": n} for name, n in modules.items()},
    }


app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(payments.router)
