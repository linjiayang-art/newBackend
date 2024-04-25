from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column,String,Integer,Text,Boolean, DateTime,BigInteger,func,BigInteger
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class BasicMode(Base):
    __abstract__ = True
    create_user=Column(String(255),default='system')
    create_date=Column(DateTime,default=func.now())
    last_modification_time=Column(DateTime,default=func.now())
    last_modification_user=Column(DateTime,default=func.now())
    is_deleted=Column(Boolean,default=False)
    def to_dict(self):
        # 使用字典推导式将对象属性转化为字典
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}