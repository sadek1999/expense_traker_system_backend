from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import sessionLocal
from schemas import UserCreate
from models import User
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY ="bf4f49c8537084cbfe6707fac797f6d417e57b402f7d97cd7808ea79f6832eac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def password_verification(plain_password: str, hash_password: str):
    return bcrypt_context.verify(plain_password, hash_password)


def create_access_toke(user_id: int, user_name: str):

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": user_name, "id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name:str = payload.get("sub")
        user_id:int = payload.get("id")

        if user_name is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user Not found",
            )

        return {"user_name": user_name, "user_id": user_id}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user Not found",
        )


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth/register")
def register_user(new_user: UserCreate, db: db_dependency):
    user = User(
        username=new_user.username,
        email=new_user.email,
        hashed_password=bcrypt_context.hash(new_user.password),
    )

    db.add(user)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "user created successfully"},
    )


@router.post("/auth/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):

    user = db.query(User).filter(User.username == form_data.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user Not found",
        )

    user_verified = password_verification(form_data.password, user.hashed_password)

    if user_verified == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_toke(user.id, user.username)

    return {"access_token": token, "token_type": "bearer"}




@router.delete("/user/{user_id}")
def delete_transaction_by_id(user_id:int, db:db_dependency):
        data=db.query(User).filter(User.id ==user_id).first()
    
        if data is None :
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="transaction is not found")

        db.delete(data)
        db.commit()

        return JSONResponse(status_code=200,content={"message":"deleted Successfully"})
