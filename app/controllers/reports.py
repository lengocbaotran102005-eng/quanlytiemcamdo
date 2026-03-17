from datetime import date

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.models.transaction import Payment, Transaction
from app.utils.decorators import admin_required


bp = Blueprint("reports", __name__, url_prefix="/reports")


@bp.route("/")
@login_required
@admin_required
def index():
    today = date.today()
    year = request.args.get("year", type=int, default=today.year)

    txs = Transaction.query.order_by(Transaction.pawn_date.desc()).all()

    payments = (
        Payment.query.filter(Payment.payment_date.between(date(year, 1, 1), date(year, 12, 31)))
        .order_by(Payment.payment_date.asc())
        .all()
    )

    monthly = []
    for month in range(1, 13):
        month_payments = [
            p
            for p in payments
            if p.payment_date.year == year and p.payment_date.month == month
        ]
        interest = sum(
            float(p.amount)
            for p in month_payments
            if p.payment_type in ("interest", "extension")
        )
        principal = sum(
            float(p.amount)
            for p in month_payments
            if p.payment_type == "redeem"
        )
        monthly.append(
            {
                "month": month,
                "interest": round(interest),
                "principal": round(principal),
            }
        )

    return render_template(
        "reports/index.html",
        transactions=txs,
        year=year,
        monthly=monthly,
    )
