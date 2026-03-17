from decimal import Decimal
from datetime import date


def calc_interest(
    pawn_value: Decimal,
    rate_monthly: Decimal,
    pawn_date: date,
    to_date: date | None = None,
) -> dict:
    if to_date is None:
        to_date = date.today()

    days = (to_date - pawn_date).days
    rate_daily = rate_monthly / Decimal("30") / Decimal("100")
    interest = pawn_value * rate_daily * days
    total = pawn_value + interest

    return {
        "days": days,
        "interest": round(interest, 0),
        "total": round(total, 0),
    }

