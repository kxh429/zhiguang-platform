"""蓝图注册"""
from flask import Flask


def register_blueprints(app: Flask):
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .assessment import assessment_bp
    from .training import training_bp
    from .report import report_bp
    from .admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
