import sqlalchemy
from  sqlalchemy import  create_engine
from Db.User import User,Base
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.exc.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base

DBName = "data.db"
'''sqlite默认建立的对象只能让建立该对象的线程使用，
而sqlalchemy是多线程的所以我们需要指定check_same_thread=False
来让建立的对象任意线程都可使用'''
Engine = create_engine('sqlite:///{0}?check_same_thread=False'.format(DBName), echo=True,encoding='utf-8')

# 1 创建表结构,表存在时，不必调用
Base.metadata.create_all(Engine)

# 创建DBSession类型:
DBSession = sessionmaker(bind=Engine)
session = DBSession();
# def insert
'''
数据操作
new_user = User(name='wangsi',password='12345')

# # 2 增
# session.add(new_user)
# session.add(new_user2)
#
# # 提交即保存到数据库:
# session.commit()

# 3 查询
my_user = session.query(User).filter_by(name='kzw').first()
# 4 修改
my_user.password = '000000';
session.commit()

print("my_user : ",my_user)
my_user = session.query(User).filter(User.name=='wangsan').all()
print("my_user : ",my_user)


# 5 多条件查询
objs = session.query(User).filter(User.id>1).filter(User.id<6).all()
print("objs : ",objs)


# 6 回滚
my_user = session.query(User).filter_by(id=1).first()
my_user.name = "Jack"
fake_user = User(name='Rain',password='12345')
session.add(fake_user)
print(session.query(User).filter(User.name.in_(['Jack','rain'])).all())
session.rollback()
print(session.query(User).filter(User.name.in_(['Jack','rain'])).all())

# 7 获取所有数据
print(session.query(User.name,User.id).all())
print(session.query(User).all())

# 8 模糊查询
like = session.query(User).filter(User.name.like('wang%')).count()
print("like : ",like)

# 9 统计和分组
# 相当于SELECT count(user.name) AS count_1, user.name AS user_name
# FROM user GROUP BY user.name
print(session.query(func.count(User.name),User.name).group_by(User.name).all())


'''