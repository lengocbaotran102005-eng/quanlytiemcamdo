from datetime import datetime

from flask_login import UserMixin

from app.extensions import bcrypt, db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.Enum("admin", "staff", name="user_roles"), nullable=False, default="staff")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    avatar_url = db.Column(db.String(255))
    email = db.Column(db.String(150), unique=True)
    bio = db.Column(db.Text)
    last_login = db.Column(db.DateTime)
    must_change_password = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    transactions_created = db.relationship(
        "Transaction",
        foreign_keys="Transaction.staff_id",
        back_populates="staff",
        lazy="dynamic",
    )
    transactions_redeemed = db.relationship(
        "Transaction",
        foreign_keys="Transaction.redeem_by",
        back_populates="redeem_staff",
        lazy="dynamic",
    )
    payments = db.relationship(
        "Payment",
        back_populates="staff",
        lazy="dynamic",
    )

    def set_password(self, raw_password: str) -> None:
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password, raw_password)

    def mark_login(self) -> None:
        self.last_login = datetime.utcnow()
