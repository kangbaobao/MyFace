from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' #表名
    id = Column(Integer,primary_key=True)
    # 用户姓名 目前数据姓名不可重复
    name = Column(String(128),unique=True)
    # cvs的md5 值
    mdfive = Column(String(64))
    #学校
    school= Column(String(64))
    # 院系
    college = Column(String(64))
    # 专业
    major = Column(String(64))
    # 班级
    classes = Column(String(64))

    def __repr__(self):
        return "<id:%s name:%s mdfive:%s>" % (self.id, self.name, self.mdfive)