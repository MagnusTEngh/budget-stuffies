from fastapi import APIRouter

from ..modules.transactions.router import router as transactions_router

router = APIRouter()

router.include_router(transactions_router)