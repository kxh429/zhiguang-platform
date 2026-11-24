"""成长报告路由"""
from flask import Blueprint, render_template, redirect, url_for, flash
from models import (
    AssessmentRecord,
    AssessmentQuestion,
    TrainingModule,
    TrainingProgress,
    DIMENSIONS,
    DIMENSION_KEYS,
)
from utils import current_user, login_required, get_dimension_level, get_dimension_advice

report_bp = Blueprint("report", __name__, url_prefix="/report")


@report_bp.route("/")
@login_required
def index():
    """报告列表"""
    user = current_user()
    records = (
        AssessmentRecord.query.filter_by(user_id=user.id, is_completed=True)
        .order_by(AssessmentRecord.completed_at.desc())
        .all()
    )

    # 为每条记录附加维度得分摘要
    for r in records:
        r.score_summary = r.dimension_scores()

    return render_template("report/index.html", records=records)


@report_bp.route("/<int:record_id>")
@login_required
def detail(record_id):
    """报告详情"""
    user = current_user()
    record = AssessmentRecord.query.get_or_404(record_id)

    if record.user_id != user.id and not user.is_admin:
        flash("无权查看此报告", "danger")
        return redirect(url_for("report.index"))

    scores = record.dimension_scores()
    total = record.total_score

    dim_data = []
    for dim_key in DIMENSION_KEYS:
        dim_info = DIMENSIONS[dim_key]
        score = scores.get(dim_key, 0)
        max_score = AssessmentQuestion.query.filter_by(dimension=dim_key).count() * 5
        dim_data.append(
            {
                "key": dim_key,
                "name": dim_info["name"],
                "color": dim_info["color"],
                "icon": dim_info["icon"],
                "desc": dim_info["desc"],
                "summary": dim_info["summary"],
                "score": score,
                "max_score": max_score,
                "pct": round(score / max_score * 100) if max_score > 0 else 0,
                "level": get_dimension_level(score, max_score),
                "advice": get_dimension_advice(dim_key, score, max_score),
            }
        )

    max_total = sum(d["max_score"] for d in dim_data)

    # 推荐训练模块：按得分百分比升序，取最低2个维度的训练
    sorted_dims = sorted(dim_data, key=lambda x: x["pct"])
    recommended = []
    for dim in sorted_dims[:2]:
        mods = (
            TrainingModule.query.filter_by(dimension=dim["key"])
            .order_by(TrainingModule.order_num)
            .all()
        )
        recommended.extend(mods)

    # 训练完成统计
    completed_training = TrainingProgress.query.filter_by(
        user_id=user.id, is_completed=True
    ).count()
    total_training = TrainingModule.query.count()

    # 历史测评趋势（最近5次）
    history_records = (
        AssessmentRecord.query.filter_by(user_id=user.id, is_completed=True)
        .order_by(AssessmentRecord.completed_at.asc())
        .limit(5)
        .all()
    )
    history_data = []
    for hr in history_records:
        hr_scores = hr.dimension_scores()
        history_data.append(
            {
                "date": hr.completed_at.strftime("%m-%d") if hr.completed_at else "--",
                "total": hr.total_score,
                "scores": hr_scores,
            }
        )

    return render_template(
        "report/detail.html",
        record=record,
        dim_data=dim_data,
        total_score=total,
        max_total=max_total,
        recommended=recommended,
        completed_training=completed_training,
        total_training=total_training,
        history_data=history_data,
    )
