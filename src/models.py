# 数据库模型定义
from flask import current_app
from src.extensions import db
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) # 主键
    username = db.Column(db.String(64), unique=True, nullable=False) # 用户名
    email = db.Column(db.String(128), unique=True, nullable=False) # 邮箱
    password = db.Column(db.String(128), nullable=False) # 密码
    is_vip = db.Column(db.Boolean, default=False) # 是否是VIP

    def __repr__(self):
        return '<User(id={}, username={}, email={}, password={}, is_vip={}))>'.format(self.id, self.username, self.email, self.password, self.is_vip)

class Paper(db.Model):
    __tablename__ = 'paper'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(255), nullable=False)  # 论文标题，最长255字符，不能为空
    abstract = db.Column(db.Text, nullable=False)  # 论文摘要,不能为空
    category = db.Column(db.String(50), nullable=True) # 论文类型
    year = db.Column(db.Integer)  # 发表年份

    def __repr__(self):
        return '<Paper(id={}, title={}, abstract={}, category={}, year={})>'.format(self.id, self.title, self.abstract, self.category, self.year)

class Citation(db.Model):
    __tablename__ = 'citations'  # 表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    citer_id = db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False)  # 引用源论文ID
    citee_id = db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False)  # 被引用论文ID

    citer = db.relationship('Paper', foreign_keys=[citer_id])  # 引用源论文
    citee = db.relationship('Paper', foreign_keys=[citee_id])  # 被引用论文

    def __repr__(self):
        return '<Citation(id={}, citer_id={}, citee_id={}, citer={}, citee={})>'.format(self.id, self.citer_id, self.citee_id, self.citer, self.citee)

class Feature(db.Model):
    __tablename__ = 'feature'  # 表名
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False, primary_key=True)  # 主键
    features = [db.Column(db.Integer, nullable=False) for i in range(128)] 


    paper = db.relationship('Paper', foreign_keys=[paper_id])  # 引用源论文

    def __repr__(self):
        return '<Citation(id={}, '.format(self.paper_id) + ", ".join(f"feat{i}={self.features[i]}" for i in range(128)) + ")>"




# 创建所有表
# 创建所有表
def create_tables():
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    tables = [User.__table__, Paper.__table__, Citation.__table__, Feature.__table__]
    for table in tables:
        if table.name not in metadata.tables:
            table.create(db.engine)

# 创建数据库会话
def create_session():
    Session = sessionmaker(bind=db.engine)
    return Session()
