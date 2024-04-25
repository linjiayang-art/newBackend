from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column,String,Integer,Text,Boolean, DateTime,BigInteger
from .basemodel import BasicMode
# from backend.models.system import BasicMode

class FileInfo(db.Model,BasicMode):
    __tablename__ = 'sys_file_info'
    id = Column(Integer, primary_key=True)
    file_path = Column(String(255))
    orginname = Column(String(255))
    localname = Column(String(255))