from backend.app.services.policy_engine import PolicyEngine


def test_policy_engine_escalates_when_required_fields_missing():
    engine = PolicyEngine()
    decision = engine.decide(
        {"action_type": "schedule_slot", "required_fields": ["first_name", "callback_number"]},
        {"first_name": "Theo"},
        {},
    )

    assert decision.escalate is True
    assert decision.confidence == 20
    assert "callback_number" in decision.rationale


def test_policy_engine_flags_urgent_ambiguous_step():
    engine = PolicyEngine()
    decision = engine.decide(
        {"action_type": "route_refill", "required_fields": ["urgency"], "ambiguity_check": True},
        {"urgency": "high"},
        {},
    )

    assert decision.escalate is True
    assert decision.confidence == 65
