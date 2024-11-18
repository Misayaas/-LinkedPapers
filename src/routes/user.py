# 用户信息
from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/profile')
def profile():
    # 用户个人资料逻辑
    pass