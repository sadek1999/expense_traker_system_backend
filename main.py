from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
import models
from database import engine,sessionLocal
from typing import Annotated
from router import auth



app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()  

db_dependency=Annotated[Session, Depends(get_db)]

app.include_router(auth.router)
@app.get("/")
def tracker():
    return ".......... welcome to the tracker .........."          


@app.post("/transactions")
def create_transactions():
    pass

@app.get("/transactions")
def read_all_transactions():
    pass

@app.get("/transactions/{transaction_id}")
def get_transactions_by_id():
    pass

@app.put("/transactions/{transaction_id}")
def update_transaction_by_id():
    pass

@app.delete("/transactions/{transaction_id}")
def delete_transaction_by_id():
    pass

@app.get("/transactions/filter")
def read_transactions_by_filter():
    pass



