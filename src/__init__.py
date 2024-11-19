import pymysql
from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, cache
from .routes.auth import auth_bp
from .routes.search import search_bp
from .routes.recommend import recommend_bp
from .routes.user import user_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)

    # 创建数据库
    with app.app_context():
        #create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(recommend_bp, url_prefix='/recommend')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
