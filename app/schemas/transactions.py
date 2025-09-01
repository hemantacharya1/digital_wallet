from pydantic import BaseModel,Optional
from datetime import datetime

from sqlalchemy import Enum

class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class TransactionBase(BaseModel):
    description = Optional[str] = None
    amount: int
    transaction_type: TransactionType

class TransactionCreate(TransactionBase):
    pass


