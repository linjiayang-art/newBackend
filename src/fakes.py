from datetime import datetime
from sqlalchemy import select,func
from src.core.extensions import db
from src.models.system import UserInfo,Menu,SysUserRole,SysRoleMenu,SysRole


def fake_admin():
    user=UserInfo(
        userno='admin',
        username='admin',
        password='123456',
    )
    db.session.add(user)
    db.session.commit()

def fake_menu():
    menu1 = Menu(id=1,  parent_id=0, menu_name='系统管理', menu_type='MENU',
                 menu_path='/system', component='Layout',
                 menu_visible=0,
                 menu_sort=1,
                 menu_icon='system',
                 redirect_url='/system/user'
                 )
    menu2 = Menu(id=2,
                 parent_id=1,
                 menu_name='菜单管理',
                 menu_type='CATALOG',
                 menu_path='menus',
                 component='system/menu/index',
                 menu_visible=0,
                 menu_sort=1,
                 menu_icon='menu',
                 )
    menu3 = Menu(
        id=3,
        parent_id=1,
        menu_name='/用户管理',
        menu_type='CATALOG',
        menu_path='/system',
        component='system/menu/user',
        menu_visible=True,
        menu_sort=3,
        menu_icon='user',
    )
    db.session.add(menu1)
    db.session.add(menu2)
    db.session.add(menu3)
    db.session.commit()

def fake_role():
    role=SysRole(
        role_name='超级管理员',
        code='admin',
        create_user='admin',
        create_date=datetime.now(),
        last_modification_time=datetime.now(),
    )
    db.session.add(role)
    db.session.commit()

def fake_role_menu():
    role=db.session.query(SysRole).scalar()
    role_id=role.id
    role1=SysRoleMenu(
        role_id=role_id,
        menu_id=1,
    )
    role2=SysRoleMenu(
        role_id=role_id,
        menu_id=2,
    )
    role3=SysRoleMenu(
        role_id=role_id,
        menu_id=3,
    )
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)
    db.session.commit()

def fake_user_role():
    user_role=SysUserRole(
        user_id=1,
        role_id=1,
    )
    db.session.add(user_role)
    db.session.commit()