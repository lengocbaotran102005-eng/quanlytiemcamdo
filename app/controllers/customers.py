from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.models.customer import Customer
from app.utils.validators import validate_phone, validate_id_card


bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/")
@login_required
def index():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template("customers/index.html", customers=customers)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        id_card = request.form.get("id_card", "").strip()
        address = request.form.get("address", "").strip()
        note = request.form.get("note", "").strip()

        if not full_name or not phone or not id_card:
            flash("Họ tên, SĐT và CCCD/CMND là bắt buộc.", "error")
            return render_template("customers/create.html")

        if not validate_phone(phone):
            flash("Số điện thoại không hợp lệ.", "error")
            return render_template("customers/create.html")

        if not validate_id_card(id_card):
            flash("CCCD/CMND không hợp lệ.", "error")
            return render_template("customers/create.html")

        customer = Customer(
            full_name=full_name,
            phone=phone,
            id_card=id_card or None,
            address=address or None,
            note=note or None,
        )
        db.session.add(customer)
        db.session.commit()
        flash("Thêm khách hàng thành công.", "success")
        return redirect(url_for("customers.index"))

    return render_template("customers/create.html")


@bp.route("/<int:customer_id>/edit", methods=["GET", "POST"])
@login_required
def edit(customer_id: int):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        id_card = request.form.get("id_card", "").strip()
        address = request.form.get("address", "").strip()
        note = request.form.get("note", "").strip()

        if not full_name or not phone or not id_card:
            flash("Họ tên, SĐT và CCCD/CMND là bắt buộc.", "error")
            return render_template("customers/edit.html", customer=customer)

        if not validate_phone(phone):
            flash("Số điện thoại không hợp lệ.", "error")
            return render_template("customers/edit.html", customer=customer)

        if not validate_id_card(id_card):
            flash("CCCD/CMND không hợp lệ.", "error")
            return render_template("customers/edit.html", customer=customer)

        customer.full_name = full_name
        customer.phone = phone
        customer.id_card = id_card
        customer.address = address or None
        customer.note = note or None
        db.session.commit()
        flash("Cập nhật khách hàng thành công.", "success")
        return redirect(url_for("customers.index"))

    return render_template("customers/edit.html", customer=customer)


@bp.route("/<int:customer_id>")
@login_required
def detail(customer_id: int):
    customer = Customer.query.get_or_404(customer_id)
    transactions = customer.transactions.order_by(customer.transactions.entity.created_at.desc()).all() if hasattr(customer.transactions, "entity") else customer.transactions.all()
    return render_template(
        "customers/detail.html",
        customer=customer,
        transactions=transactions,
    )
