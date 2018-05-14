#coding:utf-8

"""
desc:sqlalchemy使用总结
author: ben
time: 2018-05-11
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# 创建一个SQLORM基类，之后创建的表必须得继承它
base = declarative_base()

# 连接数据库，使用session用于创建程序和数据库之间的会话
ENGINE = create_engine("mysql+mysqlconnector://root:272825@localhost:3306/testsqlalchemy")

#创建Session对象
Session = sessionmaker(bind=ENGINE)

session = Session()

# 创建Users表
class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    age = Column(Integer)
    def __init__(self, name, age):
        self.name = name
        self.age = age

#初始化数据库
def init_db():
    base.metadata.create_all(ENGINE)

def drop_db():
    base.metadata.drop_all(ENGINE)


#创建新的User对象
def insert_users():
    names = {'Jeny':22, 'Lisa':18, "Mark":19}
    for key, value in names.items():
        new_user = Users(key, value)
        session.add(new_user)
    session.commit()
    session.close()

# 简单查询
def easy_query():
    users = session.query(Users.name).all()
    for item in users:
        print item

# 条件查询1
def where_query():
    # users = session.query(Users).filter(Users.age==18).all()
    users = session.query(Users).filter_by(age=18).limit(1).all()
    for item in users:
        print item.name

# 模糊匹配like
def use_like_query():
    # users = session.query(Users).filter(Users.name.like('M%')).all()
    # users = session.query(Users).filter(Users.name.like('%M%')).filter(Users.name.like('%K%'))
    # users = session.query(Users).filter((Users.name.in_(['Mary','Jeny'])))
    from sqlalchemy import or_
    users = session.query(Users).filter(or_(Users.name == 'Mark', Users.age == 19)).all()
    # print(session.query(User).filter(User.username.is_(None)).all())
    # print(session.query(User).filter(User.username.isnot(None)).all())
    for item in users:
        print item.name


if __name__ == "__main__":
    # drop_db()
    # init_db()
    # insert_users()
    #简单查询
    # easy_query()

    # 条件查询
    # where_query()

    #使用like
    use_like_query()



