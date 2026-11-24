"""后台管理路由"""
from flask import Blueprint, render_template, redirect, url_for, flash
from extensions import db
from models import User, AssessmentRecord, TrainingModule, TrainingProgress
from utils import current_user, admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def index():
    """管理首页 - 数据概览"""
    total_users = User.query.count()
    total_assessments = AssessmentRecord.query.filter_by(is_completed=True).count()
    total_modules = TrainingModule.query.count()
    total_training = TrainingProgress.query.filter_by(is_completed=True).count()

    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_records = (
        AssessmentRecord.query.filter_by(is_completed=True)
        .order_by(AssessmentRecord.completed_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/index.html",
        total_users=total_users,
        total_assessments=total_assessments,
        total_modules=total_modules,
        total_training=total_training,
        recent_users=recent_users,
        recent_records=recent_records,
    )


@admin_bp.route("/users")
@admin_required
def users():
    """用户管理"""
    all_users = User.query.order_by(User.created_at.desc()).all()

    # 为每个用户附加统计
    for u in all_users:
        u.assessment_count = AssessmentRecord.query.filter_by(
            user_id=u.id, is_completed=True
        ).count()
        u.training_count = TrainingProgress.query.filter_by(
            user_id=u.id, is_completed=True
        ).count()

    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    """切换用户管理员状态"""
    admin = current_user()
    user = User.query.get_or_404(user_id)

    if user.id == admin.id:
        flash("不能修改自己的管理员状态", "danger")
        return redirect(url_for("admin.users"))

    user.is_admin = not user.is_admin
    db.session.commit()
    action = "授予" if user.is_admin else "撤销"
    flash(f"已{action} {user.username} 的管理员权限", "success")
    return redirect(url_for("admin.users"))
