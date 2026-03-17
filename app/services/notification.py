from datetime import date

from app.models.transaction import Transaction


def get_overdue_transactions():
    today = date.today()
    return Transaction.query.filter(
        Transaction.status == "overdue",
        Transaction.due_date < today,
    ).all()

