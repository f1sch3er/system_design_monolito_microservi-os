import logging

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models
from ..auth import require_api_key
from ..storage import users_store

logger = logging.getLogger("users")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=models.User, status_code=status.HTTP_201_CREATED)
def create_user(payload: models.User):
    user = models.User(
        id=users_store.next_id(),
        nome=payload.nome,
        email=payload.email,
    )
    users_store.create(user.model_dump())
    logger.info("Usuário criado: id=%s", user.id)
    return user


@router.get("", response_model=list[models.User])
def list_users():
    return [models.User(**item) for item in users_store.all()]


@router.get("/{user_id}", response_model=models.User)
def get_user(user_id: str):
    item = users_store.get(user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return models.User(**item)


@router.put("/{user_id}", response_model=models.User)
def update_user(user_id: str, payload: models.UserUpdate):
    current = users_store.get(user_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    updated = models.User(**{**current, **payload.model_dump(exclude_unset=True)})
    users_store.update(user_id, updated.model_dump())
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    if not users_store.delete(user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    logger.info("Usuário removido: id=%s", user_id)
