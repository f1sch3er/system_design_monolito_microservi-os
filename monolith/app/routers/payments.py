import logging

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models
from ..auth import require_api_key
from ..storage import orders_store, payments_store

logger = logging.getLogger("payments")

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=models.Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payload: models.PaymentCreate):
    order = orders_store.get(payload.order_id)
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

    payment["status"] = "pago"
    payments_store.update(payment_id, payment)

    order = orders_store.get(payment["order_id"])
    if order is not None:
        order["status"] = "pago"
        orders_store.update(order["id"], order)

    logger.info("Pagamento efetivado: id=%s order=%s", payment_id, payment["order_id"])
    return models.Payment(**payment)
