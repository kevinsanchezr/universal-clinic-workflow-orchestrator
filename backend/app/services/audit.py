from sqlalchemy.orm import Session

from backend.app.models.entities import AuditLog
from backend.app.utils.logging import checksum
from backend.app.utils.redaction import redact_payload


class AuditService:
    def write(self, db: Session, event_type: str, actor_type: str, actor_id: str | None, payload: dict, run_id: str | None = None):
        redacted = redact_payload(payload)
        log = AuditLog(
            workflow_run_id=run_id,
            event_type=event_type,
            actor_type=actor_type,
            actor_id=actor_id,
            payload=redacted,
            checksum=checksum(redacted),
        )
        db.add(log)
        db.commit()
        return log
