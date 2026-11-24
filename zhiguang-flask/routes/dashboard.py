"""首页与用户仪表盘"""
from flask import Blueprint, render_template
from models import AssessmentRecord, TrainingModule, TrainingProgress
from utils import current_user, login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    user = current_user()
    if not user:
        return render_template("index.html")

    latest_record = (
        AssessmentRecord.query.filter_by(user_id=user.id, is_completed=True)
        .order_by(AssessmentRecord.completed_at.desc())
        .first()
    )

    total_modules = TrainingModule.query.count()
    completed_modules = TrainingProgress.query.filter_by(
        user_id=user.id, is_completed=True
    ).count()
    assessment_count = AssessmentRecord.query.filter_by(
        user_id=user.id, is_completed=True
    ).count()

    return render_template(
        "dashboard/index.html",
        latest_record=latest_record,
        total_modules=total_modules,
        completed_modules=completed_modules,
        assessment_count=assessment_count,
    )
