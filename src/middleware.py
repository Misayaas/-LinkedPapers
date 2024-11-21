# from flask import request, jsonify
# from functools import wraps
# from src.util.token_util import TokenUtil
from functools import wraps
import jwt
from flask import request, jsonify, g

from src.models import User

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'message': '未找到token'}), 400

    #     if token and TokenUtil.verify_token(token):
    #         request.user = TokenUtil.get_user(token)
    #         return fn(*args, **kwargs)
    #     else:
    #         return jsonify({'message': '无效的token或未登录'}), 400
    # return wrapper
        try:
            payload = jwt.decode(token, '114514', algorithms=['HS256'])
            user_id = payload.get('user_id')
            g.user = User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token已过期'}), 400
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效的token'}), 400

        return fn(*args, **kwargs)

    return wrapper

