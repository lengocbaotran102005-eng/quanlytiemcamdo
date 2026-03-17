import os

import click
from flask import Flask

from config import config as app_config
from .extensions import init_extensions, login_manager


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "default")

    app = Flask(
        __name__,
        template_folder="views",
        static_folder="static",
    )
    app.config.from_object(app_config[config_name])

    init_extensions(app)
    register_blueprints(app)
    register_login_loader()
    register_context_processors(app)
    register_cli_commands(app)

    return app


def register_blueprints(app: Flask) -> None:
    from .controllers.auth import bp as auth_bp
    from .controllers.dashboard import bp as dashboard_bp
    from .controllers.profile import bp as profile_bp
    from .controllers.customers import bp as customers_bp
    from .controllers.transactions import bp as transactions_bp
    from .controllers.items import bp as items_bp
    from .controllers.reports import bp as reports_bp
    from .controllers.users import bp as users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(users_bp)


def register_login_loader() -> None:
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        if not user_id:
            return None
        return User.query.get(int(user_id))


def register_context_processors(app: Flask) -> None:
    from .utils.helpers import format_currency, format_date, status_badge_class, status_label

    @app.context_processor
    def inject_helpers():
        return {
            "format_currency": format_currency,
            "format_date": format_date,
            "status_badge_class": status_badge_class,
            "status_label": status_label,
        }


def register_cli_commands(app: Flask) -> None:
    from datetime import date, timedelta
    from decimal import Decimal

    from .extensions import db
    from .models.customer import Customer
    from .models.item import PawnItem
    from .models.transaction import Transaction
    from .models.user import User

    @app.cli.command("seed-admin")
    def seed_admin() -> None:
        existing = User.query.filter_by(username="admin").first()
        if existing:
            click.echo("Admin user already exists.")
            return

        admin = User(
            username="admin",
            full_name="Quản lý hệ thống",
            phone="0900000000",
            role="admin",
            is_active=True,
        )
        admin.set_password("admin@123")
        admin.must_change_password = True
        db.session.add(admin)
        db.session.commit()
        click.echo("Admin user created with username=admin password=admin@123")

    @app.cli.command("seed-data")
    def seed_data() -> None:
        if Customer.query.first():
            click.echo("Sample data already exists.")
            return

        staff = User(
            username="staff1",
            full_name="Nhân viên giao dịch",
            phone="0901111111",
            role="staff",
            is_active=True,
        )
        staff.set_password("staff1@123")
        staff.must_change_password = True
        db.session.add(staff)
        db.session.flush()

        c1 = Customer(
            full_name="Nguyễn Văn A",
            phone="0901234567",
            id_card="012345678901",
            address="Quận 1, TP.HCM",
            note="Khách quen",
        )
        c2 = Customer(
            full_name="Trần Thị B",
            phone="0902345678",
            id_card="012345678902",
            address="Quận Bình Thạnh, TP.HCM",
        )
        db.session.add(c1)
        db.session.add(c2)
        db.session.flush()

        item1 = PawnItem(
            name="iPhone 14 Pro 256GB",
            category="electronics",
            brand="Apple",
            serial_number="IPH14PRO256",
            condition="good",
            estimated_value=Decimal("25000000"),
        )
        item2 = PawnItem(
            name="Nhẫn vàng 18K 2 chỉ",
            category="jewelry",
            brand="PNJ",
            condition="good",
            estimated_value=Decimal("14000000"),
        )
        db.session.add(item1)
        db.session.add(item2)
        db.session.flush()

        today = date.today()

        tx1 = Transaction(
            ticket_no="TCD-" + today.strftime("%Y%m%d") + "-001",
            customer_id=c1.id,
            item_id=item1.id,
            staff_id=staff.id,
            pawn_value=Decimal("15000000"),
            interest_rate=Decimal("3.0"),
            pawn_date=today,
            due_date=today + timedelta(days=30),
            duration_days=30,
            status="active",
        )
        tx2 = Transaction(
            ticket_no="TCD-" + today.strftime("%Y%m%d") + "-002",
            customer_id=c2.id,
            item_id=item2.id,
            staff_id=staff.id,
            pawn_value=Decimal("8000000"),
            interest_rate=Decimal("3.0"),
            pawn_date=today - timedelta(days=40),
            due_date=today - timedelta(days=10),
            duration_days=30,
            status="overdue",
        )

        db.session.add(tx1)
        db.session.add(tx2)
        db.session.commit()
        click.echo("Sample staff, customers, items, and transactions have been created.")
