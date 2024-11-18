# 检索
from flask import Blueprint

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    # 搜索逻辑
    pass