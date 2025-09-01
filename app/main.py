from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from .routers import users
from .db import Base,engine


app = FastAPI()
app.include_router(users.router)

@app.on_event("startup")
def startup():
    from .models import transactions,users
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Digital Wallet Api": "Digital Wallet Backend api's"}
