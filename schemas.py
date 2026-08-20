from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field



class TransactionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, examples=["Groceries"])
    amount: float = Field(..., gt=0, description="Amount must be greater than zero", examples=[45.50])
    type: str = Field(..., min_length=1, max_length=20, description="Transaction type, e.g., expense or income", examples=["expense"])
    category: str = Field(..., min_length=1, max_length=50, examples=["Food"])
    date: date = Field(..., examples=["2026-08-19"])





class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, examples=["Groceries"])
    amount: Optional[float] = Field(None, gt=0, examples=[50.00])
    type: Optional[str] = Field(None, min_length=1, max_length=20, examples=["expense"])
    category: Optional[str] = Field(None, min_length=1, max_length=50, examples=["Food"])
    date: Optional[date] = Field(None, examples=["2026-08-19"])






class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["johndoe"])
    email: EmailStr = Field(..., examples=["john@example.com"])


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, examples=["SecretPass123!"])


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, examples=["johndoe"])
    email: Optional[EmailStr] = Field(None, examples=["john@example.com"])
    password: Optional[str] = Field(None, min_length=8, max_length=100, examples=["NewSecretPass123!"])


