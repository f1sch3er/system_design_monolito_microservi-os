import logging
import os

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import clients, models
from .auth import require_api_key
from .storage import orders_store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("orders")

app = FastAPI(title="Orders Service")


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

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=models.Order, status_code=status.HTTP_201_CREATED)
def create_order(payload: models.OrderCreate):
    user = clients.get_user(payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    product = clients.get_product(payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    order = models.Order(
        id=orders_store.next_id(),
        user_id=payload.user_id,
        product_id=payload.product_id,
        quantidade=payload.quantidade,
        total=product["preco"] * payload.quantidade,
        status="pendente",
        user_nome=user["nome"],
        product_nome=product["nome"],
    )
    orders_store.create(order.model_dump())
    logger.info("Pedido criado: id=%s user=%s product=%s", order.id, payload.user_id, payload.product_id)
    return order


@router.get("", response_model=list[models.Order])
def list_orders():
    return [models.Order(**item) for item in orders_store.all()]


@router.get("/{order_id}", response_model=models.Order)
def get_order(order_id: str):
    item = orders_store.get(order_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return models.Order(**item)


@router.post("/{order_id}/mark-paid", response_model=models.Order)
def mark_order_paid(order_id: str):
    item = orders_store.get(order_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    item["status"] = "pago"
    orders_store.update(order_id, item)
    logger.info("Pedido marcado como pago: id=%s", order_id)
    return models.Order(**item)


@app.get("/health")
def health():
    return {"status": "ok", "service": "orders", "records": orders_store.count()}


app.include_router(router)
