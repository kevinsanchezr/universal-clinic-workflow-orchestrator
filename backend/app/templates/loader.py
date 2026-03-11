import json
from pathlib import Path


TEMPLATE_DIR = Path("/app/shared/workflow-templates")
LOCAL_TEMPLATE_DIR = Path(__file__).resolve().parents[3] / "shared" / "workflow-templates"


def load_templates() -> list[dict]:
    base_dir = TEMPLATE_DIR if TEMPLATE_DIR.exists() else LOCAL_TEMPLATE_DIR
    templates = []
    for path in sorted(base_dir.glob("*.json")):
        templates.append(json.loads(path.read_text()))
    return templates
