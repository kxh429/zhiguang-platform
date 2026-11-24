"""织光平台数据模型"""
from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# ─── 维度常量 ────────────────────────────────────────
DIMENSIONS = {
    "logic": {
        "name": "逻辑思维",
        "color": "#5B8DE6",
        "icon": "brain",
        "desc": "分析、推理、判断的能力，是理性思考的基石",
        "summary": "擅长拆解问题、识别因果、构建严密的论证链条。",
    },
    "innovation": {
        "name": "创新思维",
        "color": "#FF8C69",
        "icon": "lightbulb",
        "desc": "打破常规、产生新想法的能力，是创造力的源泉",
        "summary": "善于跨界联想、发散视角，在熟悉中发现陌生。",
    },
    "critical": {
        "name": "批判思维",
        "color": "#4ECDC4",
        "icon": "search",
        "desc": "质疑、评估、反思的能力，是独立思考的保障",
        "summary": "不盲从权威，善于辨别论据的可靠性与隐含预设。",
    },
    "system": {
        "name": "系统思维",
        "color": "#B57EDC",
        "icon": "network",
        "desc": "整体把握、关联分析的能力，是复杂问题的关键",
        "summary": "能洞察局部与整体的反馈回路，预见长远影响。",
    },
}

DIMENSION_KEYS = list(DIMENSIONS.keys())


# ─── 用户 ────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records = db.relationship("AssessmentRecord", backref="user", lazy="dynamic")
    progress = db.relationship("TrainingProgress", backref="user", lazy="dynamic")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


# ─── 测评题目 ────────────────────────────────────────
class AssessmentQuestion(db.Model):
    __tablename__ = "assessment_questions"
    id = db.Column(db.Integer, primary_key=True)
    dimension = db.Column(db.String(20), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    order_num = db.Column(db.Integer, default=0)

    answers = db.relationship("AssessmentAnswer", backref="question", lazy="dynamic")


# ─── 测评记录 ────────────────────────────────────────
class AssessmentRecord(db.Model):
    __tablename__ = "assessment_records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)

    scores = db.relationship("AssessmentScore", backref="record", lazy="dynamic", cascade="all, delete-orphan")
    answers = db.relationship("AssessmentAnswer", backref="record", lazy="dynamic", cascade="all, delete-orphan")

    def dimension_scores(self) -> dict:
        """返回 {dimension: score}"""
        return {s.dimension: s.score for s in self.scores}

    @property
    def total_score(self) -> int:
        return sum(s.score for s in self.scores)


class AssessmentScore(db.Model):
    __tablename__ = "assessment_scores"
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("assessment_records.id"), nullable=False)
    dimension = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)


class AssessmentAnswer(db.Model):
    __tablename__ = "assessment_answers"
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("assessment_records.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("assessment_questions.id"), nullable=False)
    score = db.Column(db.Integer, default=0)


# ─── 训练模块 ────────────────────────────────────────
class TrainingModule(db.Model):
    __tablename__ = "training_modules"
    id = db.Column(db.Integer, primary_key=True)
    dimension = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default="medium")
    content = db.Column(db.Text)
    tips = db.Column(db.Text)
    order_num = db.Column(db.Integer, default=0)

    progress = db.relationship("TrainingProgress", backref="module", lazy="dynamic")


class TrainingProgress(db.Model):
    __tablename__ = "training_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("training_modules.id"), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint("user_id", "module_id", name="uq_user_module"),
    )
