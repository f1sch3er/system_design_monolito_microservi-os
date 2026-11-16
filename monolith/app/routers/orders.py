import logging

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models
from ..auth import require_api_key
from ..storage import orders_store, products_store, users_store

logger = logging.getLogger("orders")

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=models.Order, status_code=status.HTTP_201_CREATED)
def create_order(payload: models.OrderCreate):
    user = users_store.get(payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    product = products_store.get(payload.product_id)
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
