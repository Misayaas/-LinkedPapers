# Flask扩展
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from sklearn.neighbors import NearestNeighbors

# 初始化
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
