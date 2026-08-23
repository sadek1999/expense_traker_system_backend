from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, sessionLocal
from typing import Annotated
from router import auth
from schemas import TransactionBase, TransactionResponse, TransactionUpdate
from models import Transaction
from fastapi.responses import JSONResponse
from router.auth import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

app.include_router(auth.router)


@app.post("/transactions")
def create_transactions(
    user: user_dependency, transactions: TransactionBase, db: db_dependency
):
    if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

    new_transaction = Transaction(**transactions.model_dump())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "created Successfully"}
    )


@app.get("/transactions")
def read_all_transactions(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return db.query(Transaction).all()


@app.get("/transactions/filter")
def read_transactions_by_filter():
    pass


@app.get("/transactions/{transaction_id}")
def get_transactions_by_id(
    user: user_dependency, transaction_id: int, db: db_dependency
):
    if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )


    my_transaction = (
        db.query(Transaction).filter(Transaction.id == transaction_id).first()
    )

    if my_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="transaction is not found"
        )

    return my_transaction


@app.put("/transactions/{transaction_id}")
def update_transaction_by_id(
    user: user_dependency,
    transaction_id: int,
    update_transaction: TransactionUpdate,
    db: db_dependency,
):
    if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
    my_transaction = (
        db.query(Transaction).filter(Transaction.id == transaction_id).first()
    )

    if my_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="transaction is not found"
        )
    updated_transaction = update_transaction.model_dump(exclude_unset=True)
    for key, value in updated_transaction.items():
        setattr(my_transaction, key, value)

    return JSONResponse(status_code=200, content={"message": "updated successfully"})


@app.delete("/transactions/{transaction_id}")
def delete_transaction_by_id(user: user_dependency, t_id: int, db: db_dependency):

    if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
    
    my_transaction = db.query(Transaction).filter(Transaction.id == t_id).first()

    if my_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="transaction is not found"
        )

    db.delete(my_transaction)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "deleted Successfully"})
