from pydantic import BaseModel
from datetime import date

# Income Schemas
class IncomeBase(BaseModel):
    date: date
    amount: float
    description: str | None = None
    payment_type: str  # cash or credit

class IncomeCreate(IncomeBase):
    pass

class IncomeOut(IncomeBase):
    id: int

    class Config:
        orm_mode = True


# Expense Schemas
class ExpenseBase(BaseModel):
    date: date
    amount: float
    category: str
    description: str | None = None
    is_regular: bool | None = True
    payment_type: str  # cash or credit

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id: int

    class Config:
        orm_mode = True
