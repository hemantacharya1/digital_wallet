from pydantic import BaseModel
from datetime import datetime

class WalletResponse(BaseModel):
    user_id: int
    balance: int
    last_update: datetime

class WalletAddBalance(BaseModel):
    amount: int
    description: str

class WalletTransaction(BaseModel):
    transaction_id : int
    user_id : int
    amount: int
    new_balance: int
    transaction_type: str