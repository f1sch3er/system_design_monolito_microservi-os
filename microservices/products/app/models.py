from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: Optional[str] = None
    nome: str
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)


class ProductUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = Field(default=None, gt=0)
    estoque: Optional[int] = Field(default=None, ge=0)
