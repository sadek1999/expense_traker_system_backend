
from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session 
from database import sessionLocal



router=APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()  
db_dependency=Annotated[Session, Depends(get_db)]


@router.post("/create_user")
def create_user():
    pass

