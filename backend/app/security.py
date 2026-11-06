from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

ALLOWED_ROLES = {"admin", "clinician", "analyst", "reception"}

def roles_required(*roles):
    allowed = set(roles)
    if not allowed.issubset(ALLOWED_ROLES):
        raise ValueError("Unknown role configured in access policy.")

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in allowed:
                return jsonify({"error": {"code": "FORBIDDEN", "message": "You do not have permission to access this resource."}}), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator

def current_user_id():
    return int(get_jwt_identity())
