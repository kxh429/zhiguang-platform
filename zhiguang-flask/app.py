"""织光平台 Flask 主应用"""
import os
from flask import Flask
from config import Config
from extensions import db
from models import DIMENSIONS


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # 确保 instance 目录存在
    instance_dir = os.path.join(app.config["BASE_DIR"], "instance")
    os.makedirs(instance_dir, exist_ok=True)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    from routes import register_blueprints
    register_blueprints(app)

    # 静态文件服务（用于访问生成的静态网站）
    @app.route('/static-site/<path:filename>')
    def serve_static_site(filename):
        from flask import send_from_directory
        static_dir = os.path.join(app.config["BASE_DIR"], "public", "static-site")
        return send_from_directory(static_dir, filename)

    # 下载静态网站压缩包
    @app.route('/download/zhiguang-static')
    def download_static_site():
        from flask import send_from_directory
        public_dir = os.path.join(app.config["BASE_DIR"], "public")
        return send_from_directory(public_dir, 'zhiguang-static.tar.gz', as_attachment=True)

    # 全局模板上下文
    @app.context_processor
    def inject_globals():
        from utils import current_user
        return {
            "DIMENSIONS": DIMENSIONS,
            "APP_NAME": Config.APP_NAME,
            "APP_SLOGAN": Config.APP_SLOGAN,
            "APP_DESC": Config.APP_DESCRIPTION,
            "current_user": current_user(),
        }

    # 创建表 + 种子数据
    with app.app_context():
        db.create_all()
        from seed import seed_database
        seed_database()

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("DEPLOY_RUN_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
