from sqlalchemy.orm import Session
from ..schemas.users import UserCreate, UserUpdate
from ..models.users import User
from fastapi import HTTPException
class UserService():

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail=f"User not found with this id {user_id}")
        else :
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail=f"User not found with this id {user_id}")
        else :
            self.db.delete(db_user)
            self.db.commit()
        return db_user
