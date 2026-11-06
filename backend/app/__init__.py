import os
from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate, jwt, cors, limiter
from .auth import auth_bp
from .api import api_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

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

    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        from .models import RevokedToken
        return db.session.get(RevokedToken, jwt_payload["jti"]) is not None

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
