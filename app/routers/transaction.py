from fastapi import APIRouter, Depends, HTTPException
from ..schemas.transactions import TransactionCreate,TransactionResponse,TransactionResponse2
from sqlalchemy.orm import Session
from ..db import get_db
from ..service import transaction

router = APIRouter(prefix='/transaction',tags=['Transaction'])

@router.post('/',response_model=TransactionResponse)
def create_transaction(sender_id:int,receiver_id:int,request: TransactionCreate, db: Session = Depends(get_db)):
    service = transaction.TransactionService(db)
    return service.create_transaction(send_user_id=sender_id, receiver_user_id=receiver_id, request=request)

@router.get('/{user_id}',response_model=list[TransactionResponse2])
def get_transaction_by_user(user_id:int,page:int,limit:int, db: Session = Depends(get_db)):
    service = transaction.TransactionService(db)
    return service.get_transactions_by_user_id(user_id=user_id,page=page,limit=limit)

@router.get('/detail/{transaction_id}', response_model=TransactionResponse2)
def get_transaction_details(transaction_id:int, db: Session = Depends(get_db)):
    service = transaction.TransactionService(db)
    return service.get_details_by_transaction_id(transaction_id=transaction_id)