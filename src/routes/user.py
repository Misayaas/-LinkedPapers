# 用户信息
from flask import Blueprint, jsonify, g, request

from src.services.auth_service import quit_user
from src.services.user_service import get_user_profile, update_user_profile, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/profile', methods=['GET'])
def get_profile():
    user = get_user_profile()
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_vip': user.is_vip
        }
        return jsonify(user_data), 200
    return jsonify({'message': '用户未登录'}), 401

@user_bp.route('/user/profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_vip = data.get('is_vip')
    user = update_user_profile(username=username, email=email, password=password, is_vip=is_vip)
    if user:
        return jsonify({'message': '更新用户信息成功'}), 200
    return jsonify({'message': '更新用户信息失败'}), 400

@user_bp.route('/user/profile', methods=['DELETE'])
def delete():
    user = delete_user()
    if user:
        quit_user()
        return jsonify({'message': '删除用户成功'}), 200
    return jsonify({'message': '删除用户失败'}), 400