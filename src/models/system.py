from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column,String,Integer,Text,Boolean, DateTime,BigInteger,func,BigInteger
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from .basemodel import BasicMode

class UserInfo(db.Model,BasicMode):
    __tablename__='user_info'
    id=Column(Integer,primary_key=True)
    userno=Column(String(255))
    username=Column(String(255))
    password_hash = Column(String(255))
    email=Column(String(255))
    
    def __str__(self) -> str:
        return self.email

    @property
    def password(self):
        raise AttributeError('Write-only property!')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Menu(db.Model,BasicMode):
    __tablename__ = 'sys_menu'
    id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger)
    menu_path = Column(String(80))
    component = Column(String(80))
    redirect_url = Column(String(80))
    menu_name = Column(String(80))  # title
    menu_icon = Column(String(80))
    menu_type = Column(String(80))
    menu_visible = Column(Boolean, default=True)
    keep_alive = Column(Boolean, default=True)
    menu_perm = Column(String(80))
    menu_sort = Column(BigInteger)

    @property
    def menu_dict(self)->dict:
        return {
            'id':self.id,
            'parent_id':self.parent_id,
            'menu_path':self.menu_path,
            'component':self.component,
            'redirect_url':self.redirect_url,
            'menu_name':self.menu_name,
            'menu_icon':self.menu_icon,
            'menu_type':self.menu_type,
            'menu_visible':self.menu_visible,
            'menu_perm':self.menu_perm
        }
    @property
    def router_dict(self) -> dict:
        return {
            "path": self.menu_path,
            "component": self.component,
            "redirect": self.redirect_url,
            "name": self.menu_path,
            "meta": {
                "title": self.menu_name,
                "icon": self.menu_icon,
                "hidden":self.menu_visible,
                "roles": [],
                "keepAlive": self.keep_alive
            }
        }


class SysRole(db.Model,BasicMode):
    __tablename__='sys_role'
    id = Column(Integer, primary_key=True)
    role_name =Column(String(50))
    code = Column(String(50))
    sort = Column(String(50))
    rolestatus = Column(String(50))

class SysRoleMenu(db.Model,BasicMode):
    __tablename__ = 'sys_role_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # relationship
    role_id = Column(BigInteger)
    menu_id = Column(BigInteger)

class SysUserRole(db.Model,BasicMode):
    __tablename__ = 'sys_user_role'
    id = Column(Integer, primary_key=True)
    # relationship
    user_id = Column(BigInteger)
    role_id = Column(BigInteger)


class DictType(db.Model, BasicMode):
    __tablename__ = 'sys_dict_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    code = Column(String(255))
    status = Column(Boolean, default=True)
    remark = Column(String(255))



class DictItem(db.Model, BasicMode):
    __tablename__ = 'sys_dict_item'
    id = Column(Integer, primary_key=True)
    type_code = Column(String(50))
    type_id = Column(String(50))
    name = Column(String(50))
    value = Column(String(50))
    status =Column(Boolean, default=True)
