from flask import jsonify
from flask_jwt_extended import jwt_required
from ..security import roles_required
from ..models import AuditEvent
from . import api_bp

@api_bp.get("/overview")
@jwt_required()
@roles_required("admin", "clinician", "analyst", "reception")
def overview():
    # Values are deliberately labelled demo metrics until a validated,
    # permission-scoped analytics data source is connected.
    return jsonify({
        "mode": "demo",
        "message": "Demo analytics only. No live hospital data is connected.",
        "kpis": [
            {"label": "Registered patients", "value": 1248, "change": "+8.2%"},
            {"label": "Appointments", "value": 386, "change": "+4.6%"},
            {"label": "Departments", "value": 12, "change": "—"},
            {"label": "Reports generated", "value": 94, "change": "+12.1%"}
        ]
    })

@api_bp.get("/admin/audit-events")
@jwt_required()
@roles_required("admin")
def audit_events():
    # Audit metadata only; never return clinical payloads or credentials.
    events = AuditEvent.query.order_by(AuditEvent.created_at.desc()).limit(100).all()
    return jsonify({"events": [
        {
            "id": event.id,
            "actor_user_id": event.actor_user_id,
            "event_type": event.event_type,
            "outcome": event.outcome,
            "created_at": event.created_at.isoformat(),
        } for event in events
    ]})
