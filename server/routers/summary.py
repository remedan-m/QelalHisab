from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from ..database import SessionLocal
from ..models import Income, Expense

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to calculate date ranges
def get_date_range(period: str):
    today = date.today()
    if period == "daily":
        start_date = today
        end_date = today
    elif period == "weekly":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == "monthly":
        start_date = today.replace(day=1)
        end_date = today.replace(day=1) + timedelta(days=31)
        end_date = end_date.replace(day=1) - timedelta(days=1)
    else:
        raise ValueError("Invalid period. Choose from 'daily', 'weekly', or 'monthly'.")
    return start_date, end_date

@router.get("/{period}")
def get_summary(period: str, db: Session = Depends(get_db)):
    """
    Retrieve income and expense summaries (cash and credit) for a given period.
    """
    try:
        start_date, end_date = get_date_range(period)
    except ValueError as e:
        return {"error": str(e)}

    # Calculate totals for cash and credit separately
    income_cash = db.query(func.sum(Income.amount)).filter(
        Income.date >= start_date, Income.date < end_date + timedelta(days=1), Income.payment_type == "cash"
    ).scalar() or 0

    income_credit = db.query(func.sum(Income.amount)).filter(
        Income.date >= start_date, Income.date < end_date + timedelta(days=1), Income.payment_type == "credit"
    ).scalar() or 0

    expense_cash = db.query(func.sum(Expense.amount)).filter(
        Expense.date >= start_date, Expense.date < end_date + timedelta(days=1), Expense.payment_type == "cash"
    ).scalar() or 0

    expense_credit = db.query(func.sum(Expense.amount)).filter(
        Expense.date >= start_date, Expense.date < end_date + timedelta(days=1), Expense.payment_type == "credit"
    ).scalar() or 0


    return {
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "income": {
            "cash": income_cash,
            "credit": income_credit,
            "total": income_cash + income_credit,
        },
        "expense": {
            "cash": expense_cash,
            "credit": expense_credit,
            "total": expense_cash + expense_credit,
        },
        "net_income": (income_cash + income_credit) - (expense_cash + expense_credit),
    }
