from datetime import date, datetime


def format_currency(value) -> str:
    if value is None:
        return ""
    return f"{float(value):,.0f}₫".replace(",", ".")


def format_date(value) -> str:
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return ""


def status_badge_class(status: str) -> str:
    mapping = {
        "active": "bg-blue-100 text-blue-700",
        "redeemed": "bg-green-100 text-green-700",
        "overdue": "bg-red-100 text-red-700",
        "extended": "bg-yellow-100 text-yellow-700",
        "liquidated": "bg-gray-100 text-gray-600",
    }
    return mapping.get(status, "bg-gray-100 text-gray-600")


def status_label(status: str) -> str:
    mapping = {
        "active": "Đang cầm",
        "redeemed": "Đã chuộc",
        "overdue": "Quá hạn",
        "extended": "Đã gia hạn",
        "liquidated": "Đã thanh lý",
    }
    return mapping.get(status, status)
