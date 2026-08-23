from datetime import date as date_type
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import Enum


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class CategoryType(str, Enum):
    FOOD = "Food"
    RENT = "Rent"
    SALARY = "Salary"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"


class TransactionBase(BaseModel):
    title: str = Field(..., min_length=1, ax_length=100, examples=["Groceries"])
    amount: float = Field(..., gt=0, description="Amount must be greater than zero", examples=[45.50])
    type: TransactionType = Field(...,description="Transaction type: expense or income",examples=[TransactionType.EXPENSE],)
    category: CategoryType = Field(...,description="Allowed transaction category",examples=[CategoryType.FOOD],)
    date: date_type = Field(..., examples=["2026-08-19"])





class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, examples=["Groceries"])
    amount: Optional[float] = Field(None, gt=0, examples=[50.00])
    type: Optional[str] = Field(None, min_length=1, max_length=20, examples=["expense"])
    category: Optional[str] = Field(None, min_length=1, max_length=50, examples=["Food"])
    date: Optional[date_type] = Field(None, examples=["2026-08-19"])


class TransactionResponse(TransactionBase):
    id: int

    # THIS IS REQUIRED for SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)



class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["johndoe"])
    email: EmailStr = Field(..., examples=["john@example.com"])


class UserCreate(UserBase):
    password: str = Field(..., examples=["test123!"])


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, examples=["johndoe"])
    email: Optional[EmailStr] = Field(None, examples=["john@example.com"])
    password: Optional[str] = Field(None, min_length=8, max_length=100, examples=["NewSecretPass123!"])


