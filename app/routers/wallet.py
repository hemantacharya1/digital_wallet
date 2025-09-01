from fastapi import APIRouter, Depends, HTTPException
from ..schemas.wallet import WalletResponse,WalletAddBalance
from sqlalchemy.orm import Session
from ..db import get_db
from ..service import wallet

router = APIRouter(prefix='/wallet',tags=['Wallet'])


@router.get('/{user_id}',response_model=WalletResponse)
def get_user_balance(user_id:int,db:Session=Depends(get_db)):
    service = wallet.WalletService(db)
    return service.get_user_balance(user_id)

@router.post('/{user_id}/add',response_model=WalletResponse)
def add_wallet_balance(user_id:int,request:WalletAddBalance,db:Session=Depends(get_db)):
    service = wallet.WalletService(db)
    return service.add_wallet_balance(user_id=user_id,request=request)
