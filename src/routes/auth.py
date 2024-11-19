# src/routes/auth.py
from flask import Blueprint, request, jsonify
from src.services.auth_service import register, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user = register(username, email, password)
    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'message': 'Username or email already exists'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = login(username, password)
    if user:
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401