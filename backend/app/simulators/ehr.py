from dataclasses import dataclass


@dataclass
class AdapterResult:
    success: bool
    trace: dict
    output: dict


class BaseEHRAdapter:
    style = "base"

    def find_screen(self, state: dict, screen_name: str) -> AdapterResult:
        return AdapterResult(True, {"screen_name": screen_name, "strategy": "deterministic"}, {"screen": screen_name})

    def locate_field(self, screen_name: str, field_name: str) -> AdapterResult:
        return AdapterResult(
            True,
            {"screen_name": screen_name, "field_name": field_name, "strategy": "selector+semantic-fallback"},
            {"field_name": field_name},
        )

    def input_value(self, field_name: str, value: str) -> AdapterResult:
        return AdapterResult(True, {"field_name": field_name, "action": "input"}, {"accepted": True, "value": value})

    def click_action(self, action_name: str) -> AdapterResult:
        return AdapterResult(True, {"action_name": action_name, "interaction": "click"}, {"clicked": True})

    def validate_result(self, expected: str) -> AdapterResult:
        return AdapterResult(True, {"expected": expected, "method": "screen-assertion"}, {"matched": True})


class ModernEHRAdapter(BaseEHRAdapter):
    style = "modern"


class LegacyEHRAdapter(BaseEHRAdapter):
    style = "legacy"

    def locate_field(self, screen_name: str, field_name: str) -> AdapterResult:
        return AdapterResult(
            True,
            {"screen_name": screen_name, "field_name": field_name, "strategy": "label-proximity+semantic-fallback"},
            {"field_name": field_name, "legacy": True},
        )


def get_adapter(style: str) -> BaseEHRAdapter:
    if style == "legacy":
        return LegacyEHRAdapter()
    return ModernEHRAdapter()
