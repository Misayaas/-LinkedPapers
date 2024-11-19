from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from src.models import User
from src.extensions import db
from flask import session
import os

# 加密解密用的密钥，最终应当隐藏起来存在一个地方，不能被人发现，以防泄露
AES_KEY = b'\xb25\xdb<\xb0W${\x8c\x01\x9c\x1bw\xb1\xb1\xcc'

# 加密算法
def encrypt_password(password):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    return b64encode(iv + encrypted_password).decode('utf-8')

# 解密算法
def decrypt_password(encrypted_password):
    encrypted_password = b64decode(encrypted_password)
    iv = encrypted_password[:16]
    encrypted_password = encrypted_password[16:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    password = unpadder.update(padded_password) + unpadder.finalize()
    return password.decode('utf-8')

def register_user(username, email, password):
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return None  # 用户名或邮箱已存在
    encrypted_password = encrypt_password(password)
    encrypted_email = encrypt_password(email)
    new_user = User(username=username, email=encrypted_email, password=encrypted_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and password == decrypt_password(user.password):
        session['user_id'] = user.id
        return user
    return None

def quit_user():
    session.clear()
    return None