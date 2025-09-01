from sqlalchemy.orm import Session
from ..models.users import User
from ..models.transactions import Transaction
from ..schemas.wallet import WalletResponse,WalletAddBalance
from fastapi import HTTPException

class WalletService():
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_balance(self,user_id:int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return WalletResponse(
                user_id=user.id,
                balance=user.balance,
                last_update=user.updated_at
            )
        else:
            raise HTTPException(status_code=404, detail=f"User not found with id {user_id}")

    def add_wallet_balance(self,user_id:int,request:WalletAddBalance):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.balance += request.amount
            self.db.commit()
            self.db.refresh(user)
            transaction = Transaction(
                user_id=user.id,
                amount=request.amount,
                transaction_type="CREDIT",
                description=request.description,
            )
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            return WalletResponse(
                user_id=user.id,
                balance=user.balance,
                last_update=user.updated_at
            )
        else:
            raise HTTPException(status_code=404, detail=f"User not found with id {user_id}")
    
    def deduct_wallet_balance(self,user_id:int,request:WalletAddBalance):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail=f"User not found with id {user_id}")
        if user.balance < request.amount:
            raise HTTPException(status_code=400, detail=f"Insufficient balance current balance: {user.balance}, required balance: {request.amount}")
        user.balance -= request.amount
        self.db.commit()
        self.db.refresh(user)
        transaction = Transaction(
            user_id=user.id,
            amount=request.amount,
            transaction_type="DEBIT",
            description=request.description,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return WalletResponse(
            user_id=user.id,
            balance=user.balance,
            last_update=user.updated_at
        )