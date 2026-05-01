from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date

from ...db.base import Base

class TransactionORM(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_type: Mapped[str] = mapped_column(String)
    account_name: Mapped[str] = mapped_column(String)
    date: Mapped[date] = mapped_column(Date)  # or Date
    category: Mapped[str] = mapped_column(String, default="Undefined")
    amount: Mapped[int] = mapped_column(Integer)