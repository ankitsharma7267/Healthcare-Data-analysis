from datetime import datetime, timezone
from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(24), nullable=False, default="analyst")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"
    jti = db.Column(db.String(36), primary_key=True)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

class AuditEvent(db.Model):
    __tablename__ = "audit_events"
    id = db.Column(db.Integer, primary_key=True)
    actor_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    event_type = db.Column(db.String(80), nullable=False, index=True)
    outcome = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    # Do not store passwords, tokens, patient identifiers, or clinical payloads here.
