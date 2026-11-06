from .extensions import db
from .models import AuditEvent

def record_event(actor_user_id, event_type, outcome):
    # Intentionally accept only bounded metadata, never request bodies or clinical data.
    db.session.add(AuditEvent(
        actor_user_id=actor_user_id,
        event_type=event_type[:80],
        outcome=outcome[:20],
    ))
    db.session.commit()
