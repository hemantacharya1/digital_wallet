from fastapi import APIRouter, Depends, HTTPException
from ..schemas.users import UserCreate,UserUpdate,UserResponse
from sqlalchemy.orm import Session
from ..db import get_db
from ..service import users

router = APIRouter(prefix='/users',tags=['Users'])


@router.post('/add',response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    service = users.UserService(db)
    return service.create_user(user)
    
@router.get('/get/{user_id}',response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    service = users.UserService(db)
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found with given id {user_id}")
    return user

@router.put('/update/{user_id}',response_model=UserResponse)
def update_user(user_id:int,user:UserUpdate,db:Session=Depends(get_db)):
    service = users.UserService(db)
    return service.update_user(user_id,user)