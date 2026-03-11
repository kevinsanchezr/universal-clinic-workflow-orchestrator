from dataclasses import dataclass


@dataclass
class PolicyDecision:
    next_action: str
    confidence: int
    rationale: str
    escalate: bool = False


class PolicyEngine:
    def decide(self, step: dict, payload: dict, state: dict) -> PolicyDecision:
        missing_required = [field for field in step.get("required_fields", []) if not payload.get(field)]
        if missing_required:
            return PolicyDecision(
                next_action="handoff",
                confidence=20,
                rationale=f"Missing required fields: {', '.join(missing_required)}",
                escalate=True,
            )

        if step.get("ambiguity_check") and payload.get("urgency") == "high":
            return PolicyDecision(
                next_action=step["action_type"],
                confidence=65,
                rationale="High urgency introduces ambiguity; continue but flag for review.",
                escalate=True,
            )

        return PolicyDecision(
            next_action=step["action_type"],
            confidence=92,
            rationale="Deterministic policy matched expected preconditions.",
            escalate=False,
        )
