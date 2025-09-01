from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Enum

class TransactionBase(BaseModel):
    description: str
    amount: int

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse2(TransactionBase):
    id:int
    transaction_type: str
    created_at: datetime
    
class TransactionResponse(BaseModel):
    transfer_id: int
    sender_transaction_id: int
    recipient_transaction_id: int
    sender_new_balance: int
    recipient_new_balance: int
    status: str
    amount:int