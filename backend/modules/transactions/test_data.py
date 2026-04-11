from .schemas import Transaction

testdata_transactions = []

testdata_transactions.append(
    Transaction(
        transaction_type="income",
        account_name="Primary account",
        date="2026-01-01",
        category="Wage",
        amount=4000,
    )
)

testdata_transactions.append(
    Transaction(
        transaction_type="expense",
        account_name="Primary account",
        date="2026-01-01",
        category="Food",
        amount=-399,
    )
)

testdata_transactions.append(
    Transaction(
        transaction_type="expense",
        account_name="Primary account",
        date="2026-01-01",
        category="Rent",
        amount=-2000,
    )
)

testdata_transactions.append(
    Transaction(
        transaction_type="internal",
        account_name="Primary account",
        date="2026-01-01",
        category="Transfer",
        amount=250,
    )
)
