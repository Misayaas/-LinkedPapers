# 用户认证
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    # 登录逻辑
    pass

@auth_bp.route('/register')
def register():
    # 注册逻辑
    pass