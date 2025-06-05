from datetime import datetime
import random
from sqlalchemy import select, func
from src.core.extensions import db
from src.models.experiment import ExperimentReport
from src.models.system import UserInfo, Menu, SysUserRole, SysRoleMenu, SysRole


def fake_admin():
    user = UserInfo(
        userno='admin',
        username='admin',
        password='123456',
    )
    db.session.add(user)
    db.session.commit()


def sys_fake_menu():
    menus = [
        Menu(
            id=111,
            parent_id=0,
            menu_name='系统管理',
            menu_type=2,
            menu_path='/system',
            component='Layout',
            keep_alive=0,
            menu_sort=1,
            menu_icon='system',
            redirect_url='/system/user'
        ),
        Menu(
            id=112,
            parent_id=111,
            menu_name='菜单管理',
            menu_type=1,
            menu_path='menus',
            component='system/menu/index',
            menu_sort=1,
            keep_alive=0,
            menu_icon='menu'
        ),
        Menu(
            id=113,
            parent_id=111,
            menu_name='用户管理',
            menu_type=1,
            menu_path='user',
            component='system/user/index',
            menu_sort=3,
            keep_alive=0,
            menu_icon='user'
        ),
        Menu(
            id=114,
            parent_id=111,
            menu_name='字典管理',
            menu_type=1,
            menu_path='dict',
            component='system/dict/index',
            route_name='Dict',
            menu_sort=3,
            keep_alive=1,
            menu_icon='user'
        ),
           Menu(
            id=116,
            parent_id=111,
            menu_name='字典项管理',
            menu_type=1,
            menu_path='dict-item',
            component='system/dict/dict-item',
            route_name='DictItem',
            menu_sort=3,
            keep_alive=0,
            menu_visible=False,
            menu_icon='user'
        ),
        Menu(
            id=115,
            parent_id=111,
            menu_name='部门',
            menu_type=1,
            menu_path='dept',
            component='system/dept/index',
            menu_sort=3,
            keep_alive=0,
            menu_icon='user'
        ),
    ]
    db.session.bulk_save_objects(menus)
    db.session.commit()


def fake_menu():
    sys_fake_menu()
    menus = [
        # 顶级菜单
        Menu(id=1, parent_id=0, menu_name='信息汇总', menu_type=2, menu_path='/info', component='Layout', menu_icon='icon-info', menu_sort=1),
        Menu(id=2, parent_id=0, menu_name='检测、认证申请', menu_type=2, menu_path='/application', component='Layout', menu_icon='icon-apply', menu_sort=2),
        Menu(id=3, parent_id=0, menu_name='进度更新', menu_type=2, menu_path='/progress', component='Layout', menu_icon='icon-progress', menu_sort=3),
        Menu(id=4, parent_id=0, menu_name='流程维护', menu_type=2, menu_path='/workflow', component='Layout', menu_icon='icon-flow', menu_sort=4),
        Menu(id=5, parent_id=0, menu_name='记录查询', menu_type=2, menu_path='/record', component='Layout', menu_icon='icon-record', menu_sort=5),
        Menu(id=6, parent_id=0, menu_name='报告查询', menu_type=2, menu_path='/report', component='Layout', menu_icon='icon-report', menu_sort=6),
        Menu(id=7, parent_id=0, menu_name='设备计量', menu_type=2, menu_path='/device-measure', component='Layout', menu_icon='icon-device', menu_sort=7),
        Menu(id=8, parent_id=0, menu_name='资产管理', menu_type=2, menu_path='/asset', component='Layout', menu_icon='icon-asset', menu_sort=8),
        Menu(id=9, parent_id=0, menu_name='设置', menu_type=2, menu_path='/settings', component='Layout', menu_icon='icon-setting', menu_sort=9),

        Menu(id=19, parent_id=5, menu_name='记录查询',route_name='recordInfo', menu_type=1, menu_path='/record', component='record/index', menu_icon='icon-record', menu_sort=5),
        # 子菜单（信息汇总）
        Menu(id=10, parent_id=1, menu_name='检测信息汇总', menu_type=1, menu_path='info-summary', component='info/summary', menu_sort=1),
        Menu(id=11, parent_id=1, menu_name='检测进度查询', menu_type=1, menu_path='progress-query', component='info/progress-query', menu_sort=2),
        Menu(id=12, parent_id=1, menu_name='设备运行汇总', menu_type=1, menu_path='device-summary', component='info/device-summary', menu_sort=3),

        # 子菜单（进度更新）
        Menu(id=13, parent_id=3, menu_name='检测、认证进度', menu_type=1, menu_path='cert-progress', component='progress/cert-progress', menu_sort=1),
        Menu(id=14, parent_id=3, menu_name='设备运行', menu_type=1, menu_path='device-run', component='progress/device-run', menu_sort=2),

        # 子菜单（流程维护）
        Menu(id=15, parent_id=4, menu_name='检测、认证项目维护', menu_type=1, menu_path='project-maintain', component='workflow/project-maintain', menu_sort=1),
        Menu(id=16, parent_id=4, menu_name='设备添减', menu_type=1, menu_path='device-change', component='workflow/device-change', menu_sort=2),

        # 子菜单（设备计量）
        Menu(id=17, parent_id=7, menu_name='台账维护', menu_type=1, menu_path='device-book', component='device/book', menu_sort=1),

        # 子菜单（资产管理）
        Menu(id=18, parent_id=8, menu_name='台账维护', menu_type=1, menu_path='asset-book', component='asset/book', menu_sort=1),
    ]

    db.session.bulk_save_objects(menus)
    db.session.commit()


def fake_role():
    role = SysRole(
        role_name='超级管理员',
        code='admin',
        create_user='admin',
        create_date=datetime.now(),
        last_modification_time=datetime.now(),
    )
    db.session.add(role)
    db.session.commit()


def fake_role_menu():
    # 获取第一个角色
    role = db.session.query(SysRole).first()
    if not role:
        raise ValueError("请先插入至少一个角色记录到 SysRole 表中")

    role_id = role.id

    # 获取所有菜单 ID
    menu_ids = db.session.query(Menu.id).all()

    # 创建角色菜单关系
    role_menus = [SysRoleMenu(role_id=role_id, menu_id=menu_id[0])
                  for menu_id in menu_ids]
    for i in role_menus:
        print(f"Role ID: {i.role_id}, Menu ID: {i.menu_id}")
    db.session.bulk_save_objects(role_menus)
    db.session.commit()


def fake_user_role():
    user_role = SysUserRole(
        user_id=1,
        role_id=1,
    )
    db.session.add(user_role)
    db.session.commit()


def fake_experiment_reports():
    test_types = ["强度测试", "老化测试", "环境测试", "稳定性测试"]
    models = ["X100", "Y200", "Z300", "A400"]
    
    for i in range(10):
        report = ExperimentReport(
            name=f"实验项目-{i+1}",
            model=random.choice(models),
            test_type=random.choice(test_types),
            report_number=f"REP-{datetime.now().strftime('%Y%m%d')}-{i+1:03}"
        )
        db.session.add(report)
    db.session.commit()

def fake_dict():
    from src.models.system import DictType,DictItem
    test_type = DictType(
        name="试验类型",
        code="test_type",
        status=True,
        remark="各种试验类型的分类"
    )
    db.session.add(test_type)
    db.session.flush()  # 提前获取 test_type.id

    # 创建字典项（试验类型子项）
    item_names = [
        "DV试验", "PV试验", "认证", "验证试验", "型式试验", "外协试验"
    ]

    dict_items = [
        DictItem(
            dict_code="test_type",
            type_id=test_type.id,
            label=name,
            value=name,
            status=True
        )
        for name in item_names
    ]

    db.session.add_all(dict_items)
    db.session.commit()