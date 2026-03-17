from datetime import date, timedelta
from decimal import Decimal

from app.services.interest import calc_interest


def test_calc_interest_zero_days():
    pawn_value = Decimal("1000000")
    rate = Decimal("3.0")
    pawn_date = date.today()
    result = calc_interest(pawn_value, rate, pawn_date, pawn_date)
    assert result["days"] == 0
    assert result["interest"] == 0
    assert result["total"] == pawn_value


def test_calc_interest_30_days():
    pawn_value = Decimal("1000000")
    rate = Decimal("3.0")
    pawn_date = date.today()
    to_date = pawn_date + timedelta(days=30)
    result = calc_interest(pawn_value, rate, pawn_date, to_date)
    assert result["days"] == 30
    assert result["interest"] == 30000
    assert result["total"] == pawn_value + 30000

