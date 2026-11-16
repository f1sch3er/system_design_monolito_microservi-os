from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Product(BaseModel):
    id: Optional[str] = None
    nome: str
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)


class ProductUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = Field(default=None, gt=0)
    estoque: Optional[int] = Field(default=None, ge=0)


class User(BaseModel):
    id: Optional[str] = None
    nome: str
    email: EmailStr


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None


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


class Payment(BaseModel):
    id: Optional[str] = None
    order_id: str
    valor: Optional[float] = None
    status: str = "pendente"


class PaymentCreate(BaseModel):
    order_id: str
