"""织光平台配置文件"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASE_DIR = BASE_DIR

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "zhiguang-platform-secret-key-2024")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'zhiguang.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # 应用元信息
    APP_NAME = "织光平台"
    APP_SLOGAN = "大学生思维破壁训练平台"
    APP_DESCRIPTION = "四维测评 · 智能训练 · 成长报告"
