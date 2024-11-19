from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User
from src.extensions import db

def register(username, email, password):
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return None  # 用户名或邮箱已存在
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None