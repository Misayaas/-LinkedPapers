# src/routes/auth.py
from debugpy.adapter import access_token
from flask import Blueprint, request, jsonify
from src.services.auth_service import register_user, login_user, quit_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user = register_user(username, email, password)
    if user:
        return jsonify({'message': '创建用户成功'}), 200
    return jsonify({'message': '用户名或邮箱已经存在'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = login_user(username, password)
    if user:
        token = create_access_token(identity=user.id)
        return jsonify({'message': '登录成功', 'token': token}), 200
    return jsonify({'message': '无效的用户名或密码'}), 400

@auth_bp.route('/quit', methods=['POST'])
def quit():
    quit_user()
    return jsonify({'message': '退出登录成功'}), 200