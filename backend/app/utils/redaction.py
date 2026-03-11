SENSITIVE_KEYS = {
    "first_name",
    "last_name",
    "full_name",
    "patient_name",
    "callback_number",
    "phone",
    "dob",
    "address",
    "member_id",
    "medication_name",
}


def redact_value(key: str, value):
    if value is None:
        return None
    if key in SENSITIVE_KEYS:
        if isinstance(value, str) and len(value) > 4:
            return f"{value[:1]}***{value[-1:]}"
        return "***"
    return value


def redact_payload(payload: dict) -> dict:
    redacted = {}
    for key, value in payload.items():
        if isinstance(value, dict):
            redacted[key] = redact_payload(value)
        elif isinstance(value, list):
            redacted[key] = [redact_payload(item) if isinstance(item, dict) else item for item in value]
        else:
            redacted[key] = redact_value(key, value)
    return redacted
