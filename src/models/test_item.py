from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey,String,Integer,Text,Boolean, DateTime,BigInteger, Unicode,func
from .basemodel import BasicMode
from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey,String,Integer,Text,Boolean, DateTime,BigInteger, Unicode, Date
from .basemodel import BasicMode


class TestSubjectInfo(db.Model,BasicMode):
    __tablename__ = 'test_subject_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False, comment="试验模型名称")
    name_cn = Column(Unicode(255), nullable=True, comment="试验模型中文名")
    description = Column(Unicode, nullable=True, comment="试验模型描述")
    version = Column(Integer, default=1, comment="版本号")
    is_used = Column(Boolean, default=True, comment="是否启用")
 

class TestItemInfo(db.Model,BasicMode): 
    __tablename__ = 'test_item_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_subject_id = Column(Integer, comment="试验模型ID")
    sort_order = Column(Integer, nullable=True, comment="排序")
    test_name =Column(Unicode(255), nullable=False, comment="试验项目")
    test_name_cn= Column(Unicode(255), nullable=True, comment="试验项目中文名")
    test_spec = Column(Unicode, nullable=False, comment="试验标准号及名称")
    test_criteria = Column(Unicode, nullable=True, comment="目标要求（评定依据）")
    sample_quantity = Column(Unicode(50), nullable=True, comment="样品数量")
    version = Column(Integer, default=1, comment="版本号")
    is_used = Column(Boolean, default=True, comment="是否启用")

class TestItemBaseInfo(db.Model,BasicMode):
    __tablename__ = 'test_item_base_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_name =Column(Unicode(255), nullable=False, comment="试验项目")
    test_name_cn= Column(Unicode(255), nullable=True, comment="试验项目中文名")
    test_spec = Column(Unicode, nullable=False, comment="试验标准号及名称")
    test_criteria = Column(Unicode, nullable=True, comment="目标要求（评定依据）")
    sample_quantity = Column(Unicode(50), nullable=True, comment="样品数量")
    created_at =Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
