"""四维测评路由"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import (
    AssessmentQuestion,
    AssessmentRecord,
    AssessmentScore,
    AssessmentAnswer,
    DIMENSIONS,
    DIMENSION_KEYS,
)
from utils import current_user, login_required, get_dimension_level, get_dimension_advice

assessment_bp = Blueprint("assessment", __name__, url_prefix="/assessment")


@assessment_bp.route("/")
@login_required
def index():
    """测评介绍页"""
    dim_counts = {}
    for dim in DIMENSION_KEYS:
        dim_counts[dim] = AssessmentQuestion.query.filter_by(dimension=dim).count()
    total_questions = AssessmentQuestion.query.count()

    user = current_user()
    history = (
        AssessmentRecord.query.filter_by(user_id=user.id, is_completed=True)
        .order_by(AssessmentRecord.completed_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "assessment/intro.html",
        dim_counts=dim_counts,
        total_questions=total_questions,
        history=history,
    )


@assessment_bp.route("/start")
@login_required
def start():
    """开始测评 - 创建记录并渲染题目"""
    questions = AssessmentQuestion.query.order_by(AssessmentQuestion.order_num).all()
    record = AssessmentRecord(user_id=current_user().id)
    db.session.add(record)
    db.session.commit()

    return render_template(
        "assessment/take.html",
        questions=questions,
        record_id=record.id,
    )


@assessment_bp.route("/submit/<int:record_id>", methods=["POST"])
@login_required
def submit(record_id):
    """提交测评"""
    record = AssessmentRecord.query.get_or_404(record_id)
    if record.user_id != current_user().id:
        flash("无权操作此测评", "danger")
        return redirect(url_for("assessment.index"))

    questions = AssessmentQuestion.query.order_by(AssessmentQuestion.order_num).all()
    dim_scores = {dim: 0 for dim in DIMENSION_KEYS}

    for q in questions:
        raw = request.form.get(f"q_{q.id}", "3")
        try:
            answer_score = max(1, min(5, int(raw)))
        except (ValueError, TypeError):
            answer_score = 3

        db.session.add(
            AssessmentAnswer(record_id=record_id, question_id=q.id, score=answer_score)
        )
        dim_scores[q.dimension] += answer_score

    for dim, score in dim_scores.items():
        db.session.add(AssessmentScore(record_id=record_id, dimension=dim, score=score))

    record.is_completed = True
    record.completed_at = datetime.utcnow()
    db.session.commit()

    flash("测评完成，来看看你的思维画像", "success")
    return redirect(url_for("assessment.result", record_id=record_id))


@assessment_bp.route("/result/<int:record_id>")
@login_required
def result(record_id):
    """测评结果"""
    record = AssessmentRecord.query.get_or_404(record_id)
    user = current_user()
    if record.user_id != user.id and not user.is_admin:
        flash("无权查看此测评结果", "danger")
        return redirect(url_for("assessment.index"))

    scores = record.dimension_scores()
    total = record.total_score

    dim_analysis = []
    for dim_key in DIMENSION_KEYS:
        dim_info = DIMENSIONS[dim_key]
        score = scores.get(dim_key, 0)
        max_score = AssessmentQuestion.query.filter_by(dimension=dim_key).count() * 5
        dim_analysis.append(
            {
                "key": dim_key,
                "name": dim_info["name"],
                "color": dim_info["color"],
                "icon": dim_info["icon"],
                "desc": dim_info["desc"],
                "score": score,
                "max_score": max_score,
                "pct": round(score / max_score * 100) if max_score > 0 else 0,
                "level": get_dimension_level(score, max_score),
                "advice": get_dimension_advice(dim_key, score, max_score),
            }
        )

    max_total = sum(a["max_score"] for a in dim_analysis)
    overall_level = get_dimension_level(total, max_total)

    return render_template(
        "assessment/result.html",
        record=record,
        dim_analysis=dim_analysis,
        total_score=total,
        max_total=max_total,
        overall_level=overall_level,
    )
