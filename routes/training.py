"""思维训练路由"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from extensions import db
from models import TrainingModule, TrainingProgress, DIMENSION_KEYS
from utils import current_user, login_required

training_bp = Blueprint("training", __name__, url_prefix="/training")


@training_bp.route("/")
@login_required
def index():
    """训练模块列表"""
    user = current_user()
    modules_by_dim = {}

    for dim in DIMENSION_KEYS:
        modules = (
            TrainingModule.query.filter_by(dimension=dim)
            .order_by(TrainingModule.order_num)
            .all()
        )
        for mod in modules:
            progress = TrainingProgress.query.filter_by(
                user_id=user.id, module_id=mod.id
            ).first()
            mod.user_completed = progress.is_completed if progress else False
        modules_by_dim[dim] = modules

    completed_count = TrainingProgress.query.filter_by(
        user_id=user.id, is_completed=True
    ).count()
    total_count = TrainingModule.query.count()

    return render_template(
        "training/index.html",
        modules_by_dim=modules_by_dim,
        completed_count=completed_count,
        total_count=total_count,
    )


@training_bp.route("/<int:module_id>")
@login_required
def module_detail(module_id):
    """训练模块详情"""
    user = current_user()
    module = TrainingModule.query.get_or_404(module_id)

    progress = TrainingProgress.query.filter_by(
        user_id=user.id, module_id=module.id
    ).first()
    is_completed = progress.is_completed if progress else False

    related = (
        TrainingModule.query.filter_by(dimension=module.dimension)
        .filter(TrainingModule.id != module.id)
        .order_by(TrainingModule.order_num)
        .all()
    )

    return render_template(
        "training/module.html",
        module=module,
        is_completed=is_completed,
        related=related,
    )


@training_bp.route("/<int:module_id>/complete", methods=["POST"])
@login_required
def complete(module_id):
    """完成训练模块"""
    user = current_user()
    module = TrainingModule.query.get_or_404(module_id)

    progress = TrainingProgress.query.filter_by(
        user_id=user.id, module_id=module.id
    ).first()

    if not progress:
        progress = TrainingProgress(user_id=user.id, module_id=module.id)
        db.session.add(progress)

    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()
        db.session.commit()
        flash(f"训练完成：{module.title}", "success")
    else:
        flash("该模块已完成", "info")

    return redirect(url_for("training.module_detail", module_id=module_id))
