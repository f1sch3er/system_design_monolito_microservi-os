from typing import Optional

from pydantic import BaseModel


class Payment(BaseModel):
    id: Optional[str] = None
    order_id: str
    valor: Optional[float] = None
    status: str = "pendente"


class PaymentCreate(BaseModel):
    order_id: str
