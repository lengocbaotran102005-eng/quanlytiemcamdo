def validate_phone(phone: str) -> bool:
    digits = "".join(ch for ch in phone if ch.isdigit())
    return 9 <= len(digits) <= 11


def validate_interest_rate(rate: float) -> bool:
    return 0 < rate <= 100


def validate_id_card(id_card: str) -> bool:
    digits = "".join(ch for ch in id_card if ch.isdigit())
    return len(digits) in (9, 12)
