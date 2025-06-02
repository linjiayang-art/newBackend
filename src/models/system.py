from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column,String,Integer,Text,Boolean, DateTime,BigInteger,func,Unicode
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
        return self.username
        # return self.email+'-'+self.username

    @property
    def password(self):
        raise AttributeError('Write-only property!')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class  Menu(db.Model,BasicMode):
    __tablename__ = 'sys_menu'
    id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger)
    menu_path = Column(Unicode(160))
    component = Column(Unicode(160))
    redirect_url = Column(Unicode(160))
    menu_name = Column(Unicode(160))  # title
    route_name= Column(Unicode(160))
    menu_icon = Column(Unicode(160))
    menu_type = Column(Integer)  # 1:菜单,2:目录,3:按钮,4:外链
    menu_visible = Column(Boolean, default=True)
    keep_alive = Column(Boolean, default=True)
    menu_perm = Column(Unicode(160))
    menu_sort = Column(BigInteger)

    @property
    def menu_dict(self)->dict:
        return {
            'id':self.id,
            'parent_id':self.parent_id,
            'parentId':self.parent_id,
            'routePath':self.menu_path,
            'component':self.component,
            'redirect':self.redirect_url,
            'name':self.menu_name,
            'icon':self.menu_icon,
            "routeName": self.route_name,
            "sort": self.menu_sort,
            'type':self.menu_type,
            'visible':self.menu_visible,
            'perm':self.menu_perm
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
                "hidden":  False if self.menu_visible else True  ,
                "roles": [],
                "keepAlive": self.keep_alive
            }
        }
    MENU_TYPE = {
        1: "MENU",     # 菜单：用于主导航栏，通常有页面组件
        2: "CATALOG",  # 目录：用于包含子菜单的中间层，通常也有页面
        3: "BUTTON",   # 按钮：操作级权限（如新增、删除），不显示为菜单
        4: "EXTLINK"   # 外链：外部链接跳转
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

class SysPerm(db.Model,BasicMode):
    __tablename__ = 'sys_perm'
    id = Column(Integer, primary_key=True)
    perm_name = Column(String(50))
    perm_code = Column(String(50))
    perm_type = Column(String(50))
    perm_url = Column(String(50))
    perm_method = Column(String(50))
    perm_status = Column(Boolean, default=True)
    perm_sort = Column(String(50))
    perm_icon = Column(String(50))
    parent_id = Column(BigInteger)

class SysRolePerm(db.Model,BasicMode):
    __tablename__ = 'sys_role_perm'
    id = Column(Integer, primary_key=True)
    role_id = Column(BigInteger)
    perm_id = Column(BigInteger)

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
