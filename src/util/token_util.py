import datetime
from flask_jwt_extended import create_access_token, decode_token
from src.models import User

class TokenUtil:
    @staticmethod
    def get_token(user):
        expires = datetime.timedelta(days=1)
        token = create_access_token(identity=user.id, expires_delta=expires)
        return token

    @staticmethod
    def verify_token(token):
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            user = User.query.get(user_id)
            if user:
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def get_user(token):
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        return User.query.get(user_id)