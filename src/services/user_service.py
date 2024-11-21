from flask import g
from src.models import User
from src.extensions import db
from src.services.auth_service import encrypt_password

# 获取当前用户的信息
def get_user_profile(user_id):
    return User.query.get(user_id)

# 更改当前用户的信息
def update_user_profile(user_id, username=None, email=None, password=None, is_vip=None):
    user = User.query.get(user_id)
    if username:
        user.username = username
    if email:
        user.email = encrypt_password(email)
    if password:
        user.password = encrypt_password(password)
    if is_vip is not None:
        user.is_vip = is_vip

    db.session.commit()
    return user

# 删除当前用户
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    g.user = None
    return user

