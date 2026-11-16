import logging

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models
from ..auth import require_api_key
from ..storage import products_store

logger = logging.getLogger("products")

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=models.Product, status_code=status.HTTP_201_CREATED)
def create_product(payload: models.Product):
    product = models.Product(
        id=products_store.next_id(),
        nome=payload.nome,
        preco=payload.preco,
        estoque=payload.estoque,
    )
    products_store.create(product.model_dump())
    logger.info("Produto criado: id=%s", product.id)
    return product


@router.get("", response_model=list[models.Product])
def list_products():
    return [models.Product(**item) for item in products_store.all()]


@router.get("/{product_id}", response_model=models.Product)
def get_product(product_id: str):
    item = products_store.get(product_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return models.Product(**item)


@router.put("/{product_id}", response_model=models.Product)
def update_product(product_id: str, payload: models.ProductUpdate):
    current = products_store.get(product_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    updated = models.Product(**{**current, **payload.model_dump(exclude_unset=True)})
    products_store.update(product_id, updated.model_dump())
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    if not products_store.delete(product_id):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    logger.info("Produto removido: id=%s", product_id)
