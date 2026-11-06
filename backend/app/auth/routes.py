import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError
from ..extensions import db, limiter
from ..models import User, RevokedToken
from ..audit import record_event
from . import auth_bp

password_hasher = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)
EMAIL_RE = re.compile(r"^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")

def error(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status

@auth_bp.post("/register")
@limiter.limit("5 per hour")
def register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    if not EMAIL_RE.match(email) or len(email) > 254:
        return error("INVALID_EMAIL", "Enter a valid email address.", 400)
    if not isinstance(password, str) or len(password) < 12 or len(password) > 128:
        return error("WEAK_PASSWORD", "Password must be 12–128 characters.", 400)
    # Public registration cannot grant privileged roles.
    user = User(email=email, password_hash=password_hasher.hash(password), role="analyst")
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("ACCOUNT_EXISTS", "An account with this email already exists.", 409)
    record_event(user.id, "account.registered", "success")
    return jsonify({"message": "Account created. You can now sign in.", "user": {"id": user.id, "email": user.email, "role": user.role}}), 201

@auth_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    user = User.query.filter_by(email=email).first()
    valid = False
    if user and user.is_active and isinstance(password, str):
        try:
            valid = password_hasher.verify(user.password_hash, password)
        except (VerifyMismatchError, InvalidHashError):
            valid = False
    if not valid:
        record_event(user.id if user else None, "auth.login", "failure")
        return error("INVALID_CREDENTIALS", "Email or password is incorrect.", 401)
    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email},
    )
    record_event(user.id, "auth.login", "success")
    return jsonify({"access_token": token, "token_type": "Bearer", "user": {"id": user.id, "email": user.email, "role": user.role}})

@auth_bp.get("/me")
@jwt_required()
def me():
    from flask_jwt_extended import get_jwt_identity
    user = db.session.get(User, int(get_jwt_identity()))
    if not user or not user.is_active:
        return error("ACCOUNT_UNAVAILABLE", "This account is unavailable.", 401)
    return jsonify({"id": user.id, "email": user.email, "role": user.role})

@auth_bp.post("/logout")
@jwt_required()
def logout():
    claims = get_jwt()
    db.session.add(RevokedToken(jti=claims["jti"]))
    db.session.commit()
    record_event(int(claims["sub"]), "auth.logout", "success")
    return jsonify({"message": "Signed out successfully."})
