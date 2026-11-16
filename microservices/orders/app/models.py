from typing import Optional

from pydantic import BaseModel, Field


class Order(BaseModel):
    id: Optional[str] = None
    user_id: str
    product_id: str
    quantidade: int = Field(gt=0)
    total: Optional[float] = None
    status: str = "pendente"
    user_nome: Optional[str] = None
    product_nome: Optional[str] = None


class OrderCreate(BaseModel):
    user_id: str
    product_id: str
    quantidade: int = Field(gt=0)
