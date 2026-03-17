from datetime import date, datetime

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    ticket_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("pawn_items.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    pawn_value = db.Column(db.Numeric(15, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    interest_type = db.Column(
        db.Enum("daily", "monthly", name="interest_types"),
        default="monthly",
    )

    pawn_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    extension_count = db.Column(db.Integer, nullable=False, default=0)

    brought_name = db.Column(db.String(100))
    brought_id_card = db.Column(db.String(20))
    brought_phone = db.Column(db.String(15))

    status = db.Column(
        db.Enum(
            "active",
            "redeemed",
            "overdue",
            "extended",
            "liquidated",
            name="transaction_status",
        ),
        nullable=False,
        default="active",
    )

    redeem_amount = db.Column(db.Numeric(15, 2))
    redeem_date = db.Column(db.Date)
    redeem_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    customer = db.relationship("Customer", back_populates="transactions")
    item = db.relationship("PawnItem", back_populates="transactions")
    staff = db.relationship(
        "User",
        foreign_keys=[staff_id],
        back_populates="transactions_created",
    )
    redeem_staff = db.relationship(
        "User",
        foreign_keys=[redeem_by],
        back_populates="transactions_redeemed",
    )
    payments = db.relationship(
        "Payment",
        back_populates="transaction",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id"),
        nullable=False,
    )
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    payment_type = db.Column(
        db.Enum(
            "interest",
            "partial",
            "redeem",
            "extension",
            name="payment_types",
        ),
        nullable=False,
    )
    payment_date = db.Column(db.Date, nullable=False, default=date.today)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transaction = db.relationship("Transaction", back_populates="payments")
    staff = db.relationship("User", back_populates="payments")
