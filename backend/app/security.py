from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from .extensions import db
from .models import User

ALLOWED_ROLES = {"admin", "clinician", "analyst", "reception"}

def roles_required(*roles):
    allowed = set(roles)
    if not allowed.issubset(ALLOWED_ROLES):
        raise ValueError("Unknown role configured in access policy.")

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            # Read current role and active status from the database so role changes
            # and account deactivation take effect without waiting for token expiry.
            user = db.session.get(User, int(get_jwt_identity()))
            if not user or not user.is_active:
                return jsonify({"error": {"code": "ACCOUNT_UNAVAILABLE", "message": "This account is unavailable."}}), 401
            if user.role not in allowed:
                return jsonify({"error": {"code": "FORBIDDEN", "message": "You do not have permission to access this resource."}}), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator

def current_user_id():
    return int(get_jwt_identity())
