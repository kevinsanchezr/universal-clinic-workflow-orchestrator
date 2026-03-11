from backend.app.utils.redaction import redact_payload


def test_redaction_masks_sensitive_fields():
    payload = {
        "first_name": "Mara",
        "callback_number": "555-1010",
        "appointment_type": "Follow-up",
    }

    redacted = redact_payload(payload)

    assert redacted["first_name"] != payload["first_name"]
    assert redacted["callback_number"] != payload["callback_number"]
    assert redacted["appointment_type"] == "Follow-up"
