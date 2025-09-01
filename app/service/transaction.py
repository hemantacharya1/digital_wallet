from sqlalchemy.orm import Session
from ..schemas.transactions import TransactionCreate,TransactionResponse
from ..models.users import User
from ..models.transactions import Transaction
from fastapi import HTTPException


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    def create_transaction(self,request:TransactionCreate,send_user_id:int, receiver_user_id:int):
        sender = self.db.query(User).filter(User.id == send_user_id).first()
        receiver = self.db.query(User).filter(User.id == receiver_user_id).first()
        if sender is None or receiver is None:
            raise HTTPException(status_code=404, detail="Invalid sender or receiver user ID")
        if sender.balance < request.amount:
            raise HTTPException(status_code=400, detail=f"Insufficient balance current balance: {sender.balance}, required balance: {request.amount}")
        transaction = Transaction(
            user_id=sender.id,
            amount=request.amount,
            transaction_type="TRANSFER_OUT",
            recipient_user_id = receiver.id,
            description = request.description
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        transaction2 = Transaction(
            user_id=receiver.id,
            amount=request.amount,
            transaction_type="TRANSFER_IN",
            recipient_user_id = receiver.id,
            reference_transaction_id = transaction.id,
            description = request.description
        )
        self.db.add(transaction2)
        self.db.commit()
        self.db.refresh(transaction2)
        transaction.reference_transaction_id = transaction2.id
        self.db.commit()
        self.db.refresh(transaction)
        #updating user balance 
        sender.balance -= request.amount
        receiver.balance += request.amount
        self.db.commit()
        self.db.refresh(sender)
        self.db.refresh(receiver)

        return TransactionResponse(
            transfer_id=transaction.id,
            sender_transaction_id=transaction.id,
            recipient_transaction_id=transaction2.id,
            sender_new_balance=sender.balance,
            recipient_new_balance=receiver.balance,
            status="Completed",
            amount=request.amount
        )

    def get_transactions_by_user_id(self,user_id:int,page:int=0,limit:int=10):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).offset(page * limit).limit(limit).all()
    
    def get_details_by_transaction_id(self,transaction_id:int):
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()