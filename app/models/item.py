from datetime import datetime

from app.extensions import db


class PawnItem(db.Model):
    __tablename__ = "pawn_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(
        db.Enum(
            "electronics",
            "jewelry",
            "vehicle",
            "documents",
            "other",
            name="item_categories",
        ),
        nullable=False,
        default="other",
    )
    brand = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    condition = db.Column(
        db.Enum("good", "fair", "poor", name="item_conditions"),
        nullable=False,
        default="good",
    )
    description = db.Column(db.Text)
    estimated_value = db.Column(db.Numeric(15, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship(
        "ItemImage",
        back_populates="item",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    transactions = db.relationship(
        "Transaction",
        back_populates="item",
        lazy="dynamic",
    )


class ItemImage(db.Model):
    __tablename__ = "item_images"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("pawn_items.id"), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    is_primary = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship("PawnItem", back_populates="images")

