from fastapi import APIRouter


router = APIRouter()


@router.get("")
def get_settings() -> dict:
    return {
        "roles": ["admin", "ops_manager", "reviewer"],
        "rbac_policy": {
            "admin": ["read", "write", "handoff.assign", "settings.manage"],
            "ops_manager": ["read", "write", "handoff.assign"],
            "reviewer": ["read", "handoff.resolve"],
        },
    }
