from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required

from app.models.transaction import Transaction


bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    today = date.today()
    total_active = Transaction.query.filter_by(status="active").count()
    total_overdue = (
        Transaction.query.filter(
            Transaction.status == "overdue",
        ).count()
    )
    due_today = (
        Transaction.query.filter(
            Transaction.due_date == today,
        ).count()
    )
    recent_transactions = (
        Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()
    )

    return render_template(
        "dashboard/index.html",
        total_active=total_active,
        total_overdue=total_overdue,
        due_today=due_today,
        recent_transactions=recent_transactions,
    )

