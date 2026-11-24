"""认证路由（注册 / 登录 / 登出）"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models import User
from utils import current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("请填写所有必填字段", "danger")
        elif len(password) < 6:
            flash("密码至少需要 6 位", "danger")
        elif User.query.filter_by(username=username).first():
            flash("该用户名已被注册", "danger")
        elif User.query.filter_by(email=email).first():
            flash("该邮箱已被注册", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            flash("注册成功，欢迎加入织光平台", "success")
            return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("登录成功", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.index"))
        else:
            flash("用户名或密码错误", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("已退出登录", "info")
    return redirect(url_for("dashboard.index"))
