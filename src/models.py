# 数据库模型定义
from src.extensions import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) # 主键
    username = db.Column(db.String(64), unique=True, nullable=False, index = True) # 用户名
    email = db.Column(db.String(128), unique=True, nullable=False, index = True) # 邮箱
    password = db.Column(db.String(128), nullable=False) # 密码
    # create_time = db.Column(db.DateTime, default=datetime.utcnow) # 创建时间
    is_vip = db.Column(db.Boolean, default=False) # 是否是VIP

    def __repr__(self):
        return '<User(id={}, username={}, email={}, password={}, is_vip={}))>'.format(self.id, self.username, self.email, self.password, self.is_vip)

class Paper(db.Model):
    __tablename__ = 'paper'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(255), nullable=False)  # 论文标题，最长255字符，不能为空
    abstract = db.Column(db.Text, nullable=False)  # 论文摘要,不能为空
    catogrory_id = db.Column(db.Integer)  # 子论文id
    publish_year = db.Column(db.Integer)  # 发表年份
    #authors = db.Column(db.String(255))  # 作者，字符串形式
    vectors = db.Column(db.PickleType)  # 论文的特征向量，使用 PickleType 存储

    def __repr__(self):
        return '<Paper(id={}, title={}, abstract={}, catogrory_id={}, publish_year={})>'.format(self.id, self.title, self.abstract, self.catogrory_id, self.publish_year)

# 引用关系模型
class Citation(db.Model):
    __tablename__ = 'citations'  # 表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    source_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)  # 引用源论文ID
    target_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)  # 被引用论文ID

    def __repr__(self):
        return '<Citation(id={}, source_id={}, target_id={})>'.format(self.id, self.source_id, self.target_id)

# 子领域模型
class Category(db.Model):
    __tablename__ = 'categories'  # 表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(100), nullable=False)  # 子领域名称

    def __repr__(self):
        return '<Category(id={}, name={})>'.format(self.id, self.name)