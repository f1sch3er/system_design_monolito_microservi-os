import logging
import os

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import clients, models
from .auth import require_api_key
from .storage import payments_store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("payments")

app = FastAPI(title="Payments Service")


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

router = APIRouter(prefix="/payments", tags=["payments"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=models.Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payload: models.PaymentCreate):
    order = clients.get_order(payload.order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    payment = models.Payment(
        id=payments_store.next_id(),
        order_id=payload.order_id,
        valor=order["total"],
        status="pendente",
    )
    payments_store.create(payment.model_dump())
    logger.info("Pagamento criado: id=%s order=%s", payment.id, payload.order_id)
    return payment


@router.get("", response_model=list[models.Payment])
def list_payments():
    return [models.Payment(**item) for item in payments_store.all()]


@router.post("/{payment_id}/pay", response_model=models.Payment)
def pay(payment_id: str):
    payment = payments_store.get(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    if payment["status"] == "pago":
        raise HTTPException(status_code=400, detail="Pagamento já realizado")

    clients.mark_order_paid(payment["order_id"])

    payment["status"] = "pago"
    payments_store.update(payment_id, payment)

    logger.info("Pagamento efetivado: id=%s order=%s", payment_id, payment["order_id"])
    return models.Payment(**payment)


@app.get("/health")
def health():
    return {"status": "ok", "service": "payments", "records": payments_store.count()}


app.include_router(router)
