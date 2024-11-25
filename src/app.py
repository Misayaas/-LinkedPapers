import os
import sys


cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")
from flask import Flask
from src import create_app
from src.routes.search import search_bp
from src.models import create_tables
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.search import search_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.services.auth_service import decrypt_password

def main():
    app = create_app()
    CORS(app)
    app.config['JWT_SECRET_KEY'] = '114514'
    jwt = JWTManager(app)

    with app.app_context():
        create_tables()

    # Register blueprints
    app.register_blueprint(auth_bp, name='auth_bp', url_prefix='/api')
    app.register_blueprint(user_bp, name='user_bp', url_prefix='/api')
    app.register_blueprint(search_bp, name='search_bp', url_prefix='/api')

    app.run(debug=True, port=8080)

if __name__ == '__main__':
    main()
