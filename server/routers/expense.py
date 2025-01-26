from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Expense
from ..schemas import ExpenseCreate, ExpenseOut

router = APIRouter(
    prefix="/expense",
    tags=["Expense"]
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ExpenseOut)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        date=expense.date,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        is_regular=expense.is_regular,
        payment_type=expense.payment_type
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/", response_model=list[ExpenseOut])
def read_expenses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Expense).offset(skip).limit(limit).all()
