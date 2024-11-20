import atexit
import os
import sys
cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")
from flask import Flask, g, session
from src import create_app
from src.models import create_tables, User
from src.routes.auth import auth_bp
from src.routes.user import user_bp

from src.services.auth_service import decrypt_password

def main():
    app = create_app()

    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            g.user = User.query.get(session['user_id'])

    # def clear_session():
    #     with app.test_request_context():
    #         session.clear()
    #
    # atexit.register(clear_session)

    with app.app_context():
        create_tables()

    # Register blueprints
    app.register_blueprint(auth_bp, name='auth_bp')
    app.register_blueprint(user_bp, name='user_bp')

    app.run(debug=True, port=8080)

if __name__ == '__main__':
    main()
