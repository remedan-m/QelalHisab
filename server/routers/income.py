from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Income
from ..schemas import IncomeCreate, IncomeOut

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=IncomeOut)
def create_income(income: IncomeCreate, db: Session = Depends(get_db)):
    db_income = Income(date=income.date, 
    amount=income.amount, 
    description=income.description,
    payment_type=income.payment_type
    )

    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

@router.get("/", response_model=list[IncomeOut])
def read_income(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Income).offset(skip).limit(limit).all()
