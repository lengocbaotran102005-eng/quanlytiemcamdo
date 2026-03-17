from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db, bcrypt
from app.models.user import User
from app.services.upload import save_avatar, delete_avatar


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/")
@login_required
def index():
    return render_template("profile/index.html")


@bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        bio = request.form.get("bio", "").strip()

        if not full_name:
            flash("Họ tên không được để trống.", "error")
            return render_template("profile/edit.html")

        if email:
            existing = User.query.filter(
                User.email == email,
                User.id != current_user.id,
            ).first()
            if existing:
                flash("Email này đã được sử dụng bởi tài khoản khác.", "error")
                return render_template("profile/edit.html")

        current_user.full_name = full_name
        current_user.phone = phone
        current_user.email = email or None
        current_user.bio = bio or None
        db.session.commit()

        flash("Cập nhật thông tin thành công!", "success")
        return redirect(url_for("profile.index"))

    return render_template("profile/edit.html")


@bp.route("/avatar", methods=["POST"])
@login_required
def upload_avatar():
    file = request.files.get("avatar")
    if not file or file.filename == "":
        flash("Vui lòng chọn ảnh.", "error")
        return redirect(url_for("profile.edit"))

    result = save_avatar(file, current_user.id)
    if not result:
        flash(
            "Ảnh không hợp lệ. Chỉ chấp nhận JPG, PNG, WEBP tối đa 2MB.",
            "error",
        )
        return redirect(url_for("profile.edit"))

    if current_user.avatar_url:
        delete_avatar(current_user.avatar_url)

    current_user.avatar_url = result["file_path"]
    db.session.commit()
    flash("Cập nhật ảnh đại diện thành công!", "success")
    return redirect(url_for("profile.index"))


@bp.route("/avatar/delete", methods=["POST"])
@login_required
def delete_avatar_route():
    if current_user.avatar_url:
        delete_avatar(current_user.avatar_url)
        current_user.avatar_url = None
        db.session.commit()
        flash("Đã xóa ảnh đại diện.", "success")
    return redirect(url_for("profile.index"))


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_pw = request.form.get("current_password", "")
        new_pw = request.form.get("new_password", "")
        confirm_pw = request.form.get("confirm_password", "")

        if not bcrypt.check_password_hash(current_user.password, current_pw):
            flash("Mật khẩu hiện tại không đúng.", "error")
            return render_template("profile/change_password.html")

        if bcrypt.check_password_hash(current_user.password, new_pw):
            flash("Mật khẩu mới không được trùng mật khẩu hiện tại.", "error")
            return render_template("profile/change_password.html")

        if new_pw != confirm_pw:
            flash("Xác nhận mật khẩu không khớp.", "error")
            return render_template("profile/change_password.html")

        errors = validate_password_strength(new_pw)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("profile/change_password.html")

        current_user.password = bcrypt.generate_password_hash(new_pw).decode("utf-8")
        current_user.must_change_password = False
        db.session.commit()
        flash("Đổi mật khẩu thành công!", "success")
        return redirect(url_for("profile.index"))

    return render_template("profile/change_password.html")


def validate_password_strength(password: str) -> list[str]:
    errors: list[str] = []
    if len(password) < 8:
        errors.append("Mật khẩu phải có ít nhất 8 ký tự.")
    if not any(c.isupper() for c in password):
        errors.append("Mật khẩu phải có ít nhất 1 chữ hoa.")
    if not any(c.isdigit() for c in password):
        errors.append("Mật khẩu phải có ít nhất 1 chữ số.")
    return errors

