from datetime import date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from flask import current_app

from app.extensions import db
from app.models.customer import Customer
from app.models.item import PawnItem
from app.models.transaction import Payment, Transaction
from app.services.interest import calc_interest
from app.services.vietqr import build_qr_url


bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@bp.route("/")
@login_required
def index():
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template("transactions/index.html", transactions=transactions)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    customers = Customer.query.order_by(Customer.full_name.asc()).all()
    if request.method == "POST":
        customer_id = int(request.form.get("customer_id"))
        item_name = request.form.get("item_name", "").strip()
        pawn_value = request.form.get("pawn_value", "0").replace(".", "")
        interest_rate = request.form.get("interest_rate", "0")
        duration_days = int(request.form.get("duration_days", "30"))
        brought_name = request.form.get("brought_name", "").strip()
        brought_id_card = request.form.get("brought_id_card", "").strip()
        brought_phone = request.form.get("brought_phone", "").strip()

        if not customer_id or not item_name:
            flash("Vui lòng chọn khách hàng và nhập thông tin tài sản.", "error")
            return render_template("transactions/create.html", customers=customers)

        pawn_value_num = float(pawn_value or 0)
        if pawn_value_num <= 0:
            flash("Số tiền cầm phải lớn hơn 0.", "error")
            return render_template("transactions/create.html", customers=customers)

        from decimal import Decimal

        pawn_item = PawnItem(
            name=item_name,
            estimated_value=pawn_value_num,
        )
        db.session.add(pawn_item)
        db.session.flush()

        pawn_date = date.today()
        due_date = pawn_date + timedelta(days=duration_days)

        ticket_no = generate_ticket_no(pawn_date)

        tx = Transaction(
            ticket_no=ticket_no,
            customer_id=customer_id,
            item_id=pawn_item.id,
            staff_id=current_user.id,
            pawn_value=Decimal(str(pawn_value_num)),
            interest_rate=Decimal(interest_rate or "0"),
            pawn_date=pawn_date,
            due_date=due_date,
            duration_days=duration_days,
            brought_name=brought_name or None,
            brought_id_card=brought_id_card or None,
            brought_phone=brought_phone or None,
        )
        db.session.add(tx)
        db.session.commit()

        flash("Tạo phiếu cầm thành công.", "success")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    return render_template("transactions/create.html", customers=customers)


@bp.route("/<int:transaction_id>")
@login_required
def detail(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    from decimal import Decimal

    today = date.today()
    if tx.status == "active" and tx.due_date < today:
        tx.status = "overdue"
        db.session.commit()

    interest_info = calc_interest(
        pawn_value=Decimal(str(tx.pawn_value)),
        rate_monthly=Decimal(str(tx.interest_rate)),
        pawn_date=tx.pawn_date,
    )
    payments = (
        tx.payments.order_by(Payment.payment_date.asc()).all()
        if tx.payments is not None
        else []
    )
    return render_template(
        "transactions/detail.html",
        tx=tx,
        interest_info=interest_info,
        last_interest_date=_last_interest_date(tx),
        payments=payments,
    )


def generate_ticket_no(pawn_date: date) -> str:
    prefix = pawn_date.strftime("TCD-%Y%m%d")

    last_tx = (
        Transaction.query.filter(
            Transaction.ticket_no.like(f"{prefix}-%")
        )
        .order_by(Transaction.ticket_no.desc())
        .first()
    )

    if last_tx and last_tx.ticket_no:
        try:
            last_number = int(last_tx.ticket_no.rsplit("-", 1)[-1])
        except ValueError:
            last_number = 0
    else:
        last_number = 0

    next_number = last_number + 1
    while True:
        ticket_no = f"{prefix}-{next_number:03d}"
        exists = Transaction.query.filter_by(ticket_no=ticket_no).first()
        if not exists:
            return ticket_no
        next_number += 1


def _last_interest_date(tx: Transaction) -> date:
    last_payment = (
        tx.payments.filter(Payment.payment_type.in_(["interest", "extension"]))
        .order_by(Payment.payment_date.desc())
        .first()
    )
    return last_payment.payment_date if last_payment else tx.pawn_date


@bp.route("/<int:transaction_id>/interest", methods=["POST"])
@login_required
def pay_interest(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    from decimal import Decimal

    today = date.today()

    # Chỉ cho thu lãi đúng ngày hạn chuộc, khi phiếu chưa quá hạn
    if today < tx.due_date:
        flash("Chưa đến hạn, không thể thu lãi kỳ này.", "info")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))
    if today > tx.due_date:
        flash("Phiếu đã quá hạn, chỉ được tất toán hoặc gia hạn.", "error")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    start_date = _last_interest_date(tx)
    to_date = today
    info = calc_interest(
        pawn_value=Decimal(str(tx.pawn_value)),
        rate_monthly=Decimal(str(tx.interest_rate)),
        pawn_date=start_date,
        to_date=to_date,
    )
    amount = info["interest"]

    if amount <= 0:
        flash("Không có lãi phải thu.", "info")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    p = Payment(
        transaction_id=tx.id,
        staff_id=current_user.id,
        amount=Decimal(str(amount)),
        payment_type="interest",
        payment_date=to_date,
        note=f"Thu lãi từ {start_date.strftime('%d/%m/%Y')} đến {to_date.strftime('%d/%m/%Y')}",
    )
    db.session.add(p)
    db.session.commit()
    flash("Đã ghi nhận thu lãi tháng.", "success")
    return redirect(url_for("transactions.detail", transaction_id=tx.id))


@bp.route("/<int:transaction_id>/interest/qr")
@login_required
def qr_interest(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    from decimal import Decimal

    today = date.today()
    if today < tx.due_date:
        flash("Chưa đến hạn, không thể thu lãi kỳ này.", "info")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))
    if today > tx.due_date:
        flash("Phiếu đã quá hạn, chỉ được tất toán hoặc gia hạn.", "error")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    start_date = _last_interest_date(tx)
    info = calc_interest(
        pawn_value=Decimal(str(tx.pawn_value)),
        rate_monthly=Decimal(str(tx.interest_rate)),
        pawn_date=start_date,
        to_date=today,
    )
    amount = int(info["interest"])
    if amount <= 0:
        flash("Không có lãi phải thu.", "info")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    qr_url = build_qr_url(amount, f"thanh toan lai {tx.ticket_no}")

    return render_template(
        "transactions/qr_interest.html",
        tx=tx,
        amount=amount,
        qr_url=qr_url,
    )


@bp.route("/<int:transaction_id>/extend", methods=["POST"])
@login_required
def extend(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    from decimal import Decimal

    max_extensions = current_app.config.get("MAX_EXTENSIONS_PER_TICKET", 3)
    if tx.extension_count >= max_extensions:
        flash("Phiếu này đã đạt số lần gia hạn tối đa.", "error")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    today = date.today()
    if today > tx.due_date:
        flash("Phiếu đã quá hạn, không thể gia hạn. Vui lòng tất toán.", "error")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    try:
        extra_days = int(request.form.get("extension_days", "30"))
    except ValueError:
        extra_days = 30
    if extra_days <= 0:
        extra_days = 30

    start_date = _last_interest_date(tx)
    to_date = today

    days_passed = (to_date - start_date).days
    if days_passed <= 0:
        # Nếu vừa tạo phiếu/gia hạn trong ngày, vẫn thu lãi cho kỳ gia hạn (mặc định 30 ngày)
        effective_start = to_date - timedelta(days=extra_days)
    else:
        effective_start = start_date

    info = calc_interest(
        pawn_value=Decimal(str(tx.pawn_value)),
        rate_monthly=Decimal(str(tx.interest_rate)),
        pawn_date=effective_start,
        to_date=to_date,
    )
    amount = info["interest"]

    tx.due_date = tx.due_date + timedelta(days=extra_days)
    tx.duration_days = tx.duration_days + extra_days
    tx.status = "extended"
    tx.extension_count = tx.extension_count + 1

    p = Payment(
        transaction_id=tx.id,
        staff_id=current_user.id,
        amount=Decimal(str(amount)),
        payment_type="extension",
        payment_date=to_date,
        note=f"Gia hạn thêm {extra_days} ngày, thu lãi kỳ trước",
    )
    db.session.add(p)
    db.session.commit()
    flash("Đã gia hạn phiếu và thu lãi kỳ trước.", "success")
    return redirect(url_for("transactions.detail", transaction_id=tx.id))


@bp.route("/<int:transaction_id>/redeem", methods=["POST"])
@login_required
def redeem(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    from decimal import Decimal

    today = date.today()
    info = calc_interest(
        pawn_value=Decimal(str(tx.pawn_value)),
        rate_monthly=Decimal(str(tx.interest_rate)),
        pawn_date=_last_interest_date(tx),
        to_date=today,
    )
    interest_amount = info["interest"]
    total = Decimal(str(tx.pawn_value)) + Decimal(str(interest_amount))

    tx.redeem_amount = Decimal(str(total))
    tx.redeem_date = today
    tx.redeem_by = current_user.id
    tx.status = "redeemed"

    p = Payment(
        transaction_id=tx.id,
        staff_id=current_user.id,
        amount=Decimal(str(total)),
        payment_type="redeem",
        payment_date=today,
        note=f"Chuộc đồ - tất toán phiếu, gồm gốc và lãi còn lại",
    )
    db.session.add(p)
    db.session.commit()
    flash("Đã tất toán phiếu và ghi nhận chuộc đồ.", "success")
    return redirect(url_for("transactions.detail", transaction_id=tx.id))


@bp.route("/<int:transaction_id>/print")
@login_required
def print_ticket(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    return render_template("transactions/print_ticket.html", tx=tx)


@bp.route("/<int:transaction_id>/print-redeem")
@login_required
def print_redeem(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    payment = (
        tx.payments.filter(Payment.payment_type == "redeem")
        .order_by(Payment.payment_date.desc())
        .first()
    )
    if payment is None:
        flash("Phiếu này chưa được tất toán để in phiếu chuộc.", "info")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))
    return render_template("transactions/print_redeem.html", tx=tx, payment=payment)


@bp.route("/<int:transaction_id>/redeem/qr")
@login_required
def qr_redeem(transaction_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    from decimal import Decimal

    today = date.today()
    info = calc_interest(
        pawn_value=Decimal(str(tx.pawn_value)),
        rate_monthly=Decimal(str(tx.interest_rate)),
        pawn_date=_last_interest_date(tx),
        to_date=today,
    )
    interest_amount = info["interest"]
    total = Decimal(str(tx.pawn_value)) + Decimal(str(interest_amount))
    amount = int(total)

    if amount <= 0:
        flash("Không có số tiền phải thu để tất toán.", "info")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))

    qr_url = build_qr_url(amount, f"tat toan phieu {tx.ticket_no}")

    return render_template(
        "transactions/qr_redeem.html",
        tx=tx,
        amount=amount,
        qr_url=qr_url,
    )


@bp.route("/<int:transaction_id>/payments/<int:payment_id>/print")
@login_required
def print_payment(transaction_id: int, payment_id: int):
    tx = Transaction.query.get_or_404(transaction_id)
    payment = Payment.query.get_or_404(payment_id)
    if payment.transaction_id != tx.id:
        flash("Phiếu thu không thuộc giao dịch này.", "error")
        return redirect(url_for("transactions.detail", transaction_id=tx.id))
    return render_template("transactions/print_payment.html", tx=tx, payment=payment)
