from flask import Blueprint, render_template
from flask_login import login_required

from app.models.item import PawnItem


bp = Blueprint("items", __name__, url_prefix="/items")


@bp.route("/")
@login_required
def index():
    items = PawnItem.query.order_by(PawnItem.created_at.desc()).all()
    return render_template("items/index.html", items=items)

