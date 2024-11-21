# 用户信息
from flask import Blueprint, jsonify, request, g
from src.services.user_service import update_user_profile, delete_user
from src.middleware import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/profile', methods=['GET'])
@login_required
def get_profile():
    user = g.user
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_vip': user.is_vip
        }
        return jsonify(user_data), 200
    return jsonify({'message': '用户未登录'}), 400

@user_bp.route('/user/profile', methods=['POST'])
@login_required
def update_profile():
    # user = g.user
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
@login_required
def delete():
    # user = request.user
    if delete_user():
        return jsonify({'message': '删除用户成功'}), 200
    return jsonify({'message': '删除用户失败'}), 400