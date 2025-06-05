from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey,String,Integer,Text,Boolean, DateTime,BigInteger, Unicode
from .basemodel import BasicMode


class ExperimentReport(db.Model,BasicMode):
    __tablename__ = 'experiment_report'  # 表名建议使用下划线风格

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255),  comment='名称')
    model = Column(Unicode(255), comment='型号')
    test_type = Column(Unicode(255),  comment='试验类型')
    report_number = Column(Unicode(255), unique=True, comment='报告编号')
    file_url = Column(String(255),  comment='文件地址')