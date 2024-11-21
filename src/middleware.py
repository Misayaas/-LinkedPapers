from flask import request, jsonify
from functools import wraps
from src.util.token_util import TokenUtil

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if token and TokenUtil.verify_token(token):
            request.user = TokenUtil.get_user(token)
            return fn(*args, **kwargs)
        else:
            return jsonify({'message': '无效的token或未登录'}), 400
    return wrapper