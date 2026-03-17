from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models.user import User


bp = Blueprint("auth", __name__, url_prefix="")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username, is_active=True).first()
        if user is None or not user.check_password(password):
            flash("Sai tên đăng nhập hoặc mật khẩu.", "error")
            return render_template("auth/login.html")

        login_user(user)
        user.mark_login()
        db.session.commit()

        return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
