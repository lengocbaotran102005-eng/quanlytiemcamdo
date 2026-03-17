from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.user import User
from app.utils.decorators import admin_required


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/")
@login_required
@admin_required
def index():
    users = User.query.filter_by(is_deleted=False).order_by(User.created_at.desc()).all()
    return render_template("users/index.html", users=users)


@bp.route("/new", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        role = request.form.get("role", "staff")

        if not username or not full_name:
            flash("Tên đăng nhập và họ tên là bắt buộc.", "error")
            return render_template("users/new.html")

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Tên đăng nhập đã tồn tại.", "error")
            return render_template("users/new.html")

        if role not in ("admin", "staff"):
            role = "staff"

        user = User(
            username=username,
            full_name=full_name,
            phone=phone or None,
            role=role,
            is_active=True,
            is_deleted=False,
        )
        temp_password = f"{username}@123"
        user.set_password(temp_password)
        user.must_change_password = True
        db.session.add(user)
        db.session.commit()

        flash(f"Tạo nhân viên thành công. Mật khẩu tạm: {temp_password}", "success")
        return redirect(url_for("users.index"))

    return render_template("users/new.html")


@bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(user_id: int):
    user = User.query.get_or_404(user_id)
    if user.is_deleted:
        flash("Tài khoản này đã bị xóa.", "error")
        return redirect(url_for("users.index"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()

        if not full_name:
            flash("Họ tên không được để trống.", "error")
            return render_template("users/edit.html", user=user)

        user.full_name = full_name
        user.phone = phone or None
        db.session.commit()
        flash("Cập nhật nhân viên thành công.", "success")
        return redirect(url_for("users.index"))

    return render_template("users/edit.html", user=user)


@bp.route("/<int:user_id>/toggle", methods=["POST"])
@login_required
@admin_required
def toggle(user_id: int):
    user = User.query.get_or_404(user_id)

    if user.role == "admin":
        flash("Không thể khóa/mở khóa tài khoản quản lý.", "error")
        return redirect(url_for("users.index"))

    if user.id == current_user.id:
        flash("Không thể khóa tài khoản đang đăng nhập.", "error")
        return redirect(url_for("users.index"))

    user.is_active = not user.is_active
    db.session.commit()
    flash("Cập nhật trạng thái nhân viên thành công.", "success")
    return redirect(url_for("users.index"))


@bp.route("/<int:user_id>/reset-password", methods=["POST"])
@login_required
@admin_required
def reset_password(user_id: int):
    user = User.query.get_or_404(user_id)

    if user.role == "admin" and user.id != current_user.id:
        flash("Không được reset mật khẩu admin khác trực tiếp.", "error")
        return redirect(url_for("users.index"))

    temp_password = f"{user.username}@123"
    user.set_password(temp_password)
    user.must_change_password = True
    db.session.commit()
    flash(f"Mật khẩu đã được reset về: {temp_password}", "success")
    return redirect(url_for("users.index"))


@bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def soft_delete(user_id: int):
    user = User.query.get_or_404(user_id)

    if user.role == "admin":
        flash("Không thể xóa tài khoản quản lý.", "error")
        return redirect(url_for("users.index"))

    if user.id == current_user.id:
        flash("Không thể xóa tài khoản đang đăng nhập.", "error")
        return redirect(url_for("users.index"))

    user.is_active = False
    user.is_deleted = True
    db.session.commit()
    flash("Đã xóa mềm tài khoản nhân viên.", "success")
    return redirect(url_for("users.index"))
