"""通用工具函数"""
from functools import wraps
from flask import session, redirect, url_for, flash, abort
from models import User, DIMENSIONS


def current_user():
    """获取当前登录用户对象，未登录返回 None"""
    uid = session.get("user_id")
    if uid:
        return User.query.get(uid)
    return None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录后继续", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录", "warning")
            return redirect(url_for("auth.login"))
        user = User.query.get(session["user_id"])
        if not user or not user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapper


def get_dimension_level(score: int, max_score: int = 50) -> str:
    """根据维度得分返回等级"""
    pct = score / max_score * 100
    if pct >= 85:
        return "卓越"
    elif pct >= 70:
        return "优秀"
    elif pct >= 55:
        return "良好"
    elif pct >= 40:
        return "中等"
    else:
        return "待提升"


def get_dimension_advice(dimension: str, score: int, max_score: int = 50) -> str:
    """根据维度和得分返回个性化建议"""
    pct = score / max_score * 100
    dim_info = DIMENSIONS.get(dimension, {})
    name = dim_info.get("name", dimension)

    if pct >= 85:
        return f"你的{name}已达到卓越水平，继续保持并尝试挑战更高难度的训练。可考虑指导他人来巩固理解。"
    elif pct >= 70:
        return f"你的{name}表现优秀，基础扎实。建议在薄弱环节进行针对性提升，向卓越迈进。"
    elif pct >= 55:
        return f"你的{name}处于良好水平，有不错的潜力。通过系统训练可以快速提升到优秀水平。"
    elif pct >= 40:
        return f"你的{name}有提升空间，建议从基础训练模块开始，循序渐进地加强。"
    else:
        return f"你的{name}目前处于起步阶段，不必气馁。坚持每日练习，从简单模块开始建立信心。"
