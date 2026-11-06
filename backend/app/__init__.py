import os
import click
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, jsonify, request
from .config import Config
from .extensions import db, migrate, jwt, cors, limiter
from .auth import auth_bp
from .api import api_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config.get("TESTING") and (not app.config.get("SECRET_KEY") or not app.config.get("JWT_SECRET_KEY")):
        raise RuntimeError("Set SECRET_KEY and JWT_SECRET_KEY in the environment before starting HealthPulse.")
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"].split(",")}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    )
    limiter.init_app(app)

    from . import models  # noqa: F401
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    def request_path_is_api(response):
        # Keep API responses containing account or analytics data out of browser caches.
        return request.path.startswith("/api/")

    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        from .models import RevokedToken
        return db.session.get(RevokedToken, jwt_payload["jti"]) is not None

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if request_path_is_api(response):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.cli.command("promote-user")
    @click.argument("email")
    @click.option("--role", type=click.Choice(["admin", "clinician", "analyst", "reception"]), required=True)
    def promote_user(email, role):
        """Assign a role to an existing account from a trusted server shell."""
        from .models import User
        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user:
            raise click.ClickException("User not found. Register the account first.")
        user.role = role
        db.session.commit()
        click.echo(f"Updated {user.email} to role: {role}")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "healthpulse-api"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Resource not found."}}), 404

    @app.errorhandler(429)
    def rate_limited(_error):
        return jsonify({"error": {"code": "RATE_LIMITED", "message": "Too many requests. Try again later."}}), 429

    return app
