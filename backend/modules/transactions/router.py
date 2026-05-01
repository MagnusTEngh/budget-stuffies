import logging

from fastapi import APIRouter, Depends, HTTPException
from ...core.database import get_db
from sqlalchemy.orm import Session

from .schemas import Transaction
from .models import TransactionORM

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transaction", tags=["transaction"])

def date_filter(transactions, from_date = None, to_date = None):
    if from_date:
        transactions.filter(TransactionORM.date > from_date)
    if to_date:
        transactions.filter(TransactionORM.date < to_date)
    return transactions

@router.get("/all", response_model=list[Transaction])
def get_all_transactions(from_date = None, to_date = None, db: Session = Depends(get_db)):
    transactions = db.query(TransactionORM)
    if from_date or to_date:
        transactions = date_filter(transactions, from_date, to_date)
    if transactions:
        return transactions.all()
    raise HTTPException(status_code=404, detail="No transactions found.")



@router.get("/income")
def get_incomes(from_date = None, to_date = None, db: Session = Depends(get_db)):
    transactions = db.query(TransactionORM).filter(TransactionORM.transaction_type == "income")
    if from_date or to_date:
        transactions = date_filter(transactions, from_date, to_date)
    if transactions:
        return transactions.all()
    raise HTTPException(status_code=404, detail="No transactions found.")

@router.get("/expense")
def get_expenses(db: Session = Depends(get_db)):
    transactions = db.query(TransactionORM).filter(TransactionORM.transaction_type == "expense")
    if transactions:
        return transactions.all()
    raise HTTPException(status_code=404, detail="No transactions found.")

@router.get("/internal")
def get_internal_transactions(db: Session = Depends(get_db)):
    transactions = db.query(TransactionORM).filter(TransactionORM.transaction_type == "internal")
    if transactions:
        return transactions.all()
    raise HTTPException(status_code=404, detail="No transactions found.")
