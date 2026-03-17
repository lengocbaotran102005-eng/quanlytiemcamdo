from urllib.parse import quote_plus

from flask import current_app


def build_qr_url(amount: int, description: str) -> str:
    bank_code = current_app.config.get("VIETQR_BANK", "techcombank")
    account_number = current_app.config.get("VIETQR_ACCOUNT", "")
    account_name = current_app.config.get("VIETQR_ACCOUNT_NAME", "")
    template = "compact2"

    base = f"https://img.vietqr.io/image/{bank_code}-{account_number}-{template}.jpg"
    add_info = quote_plus(description)
    account_name_encoded = quote_plus(account_name)

    return f"{base}?amount={amount}&addInfo={add_info}&accountName={account_name_encoded}"

