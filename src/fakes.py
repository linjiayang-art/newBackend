from datetime import datetime
import random
from sqlalchemy import select, func
from src.core.extensions import db
from src.models.experiment import ExperimentReport
from src.models.system import UserInfo, Menu, SysUserRole, SysRoleMenu, SysRole
from src.models.test_item import TestItemBaseInfo


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
        Menu(id=15, parent_id=4, menu_name='检测、认证项目维护', menu_type=1, menu_path='project-maintain', component='workFlowTemplate/index',route_name='workFlowTemplate', menu_sort=1),
        Menu(id=16, parent_id=4, menu_name='设备添减', menu_type=1, menu_path='device-change', component='device/index', menu_sort=2),
         Menu(id=155, parent_id=4, menu_name='检验项目明细维护', menu_type=1, menu_path='project-maintain-detail', component='workFlowTemplate/templateInfo/index', menu_sort=1),
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
    device_status = DictType(
        name="设备状态",
        code="device_status",
        status=True,
        remark="各种设备状态的分类"
    )
    db.session.add(device_status)
    db.session.flush()  # 提前获取 test_type.id
    # 创建字典项（试验类型子项）
    item_names = [
       "运行","维修","待机","报废"
    ]

    device_status_items = [
        DictItem(
            dict_code="device_status",
            type_id=test_type.id,
            label=name,
            value=name,
            status=True
        )
        for name in item_names
    ]

    db.session.add_all(device_status_items)
    db.session.commit()

def fake_device():
    from src.models.devicemodel import Device
    import pandas as pd 
    '"D:\A-A-P\newBackend\modelfile\检测中心设备台账.xlsx"'
    file_path= r"D:\A-A-P\newBackend\modelfile\检测中心设备台账.xlsx"
    field_name_map = {
    "id": "序号",
    "manage_code": "管理编号",
    "device_type": "设备类型",
    "device_name": "设备名称",
    "device_model": "设备型号",
    "serial_number": "出厂编号",
    "manufacturer": "制造厂商",
    "management_department": "管理部门",
    "location": "放置位置",
    "start_date": "起用时间",
    "check_cycle": "校准/检查周期",
    "last_check_date": "最近检定/完好评定日期",
    "status": "使用状态",
    "check_type": "计量校准/完好评定",
    "next_check_date": "有效期/下次检查日期",
    "metering_property": "计量特性",
    "unit": "计量单位",
    "remarks": "备注"
    }
    df = pd.read_excel(file_path, sheet_name='监视和测量设备台账', header=0)
 
    df_dict= df.to_dict(orient='records')
    for row in df_dict:
        device_data = {}
        device_data = {key: row[field_name_map[key]] for key in field_name_map.keys()}
        #替换nan为\
        for key, value in device_data.items():
            if pd.isna(value):
                device_data[key] = ''
            elif isinstance(value, str):
                device_data[key] = value.strip()
            elif isinstance(value, datetime):
                device_data[key] = value.date()
        try:
            device = Device(**device_data)
            db.session.add(device)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding device: {e}, data: {device_data}")
  
 

def fake_test_items():
    # Data extracted from the provided document, including Chinese test names
    test_items = [
        {
            "test_name": "Visual Inspection",
            "test_name_cn": "外观检查",
            "test_spec": "1、按SAE/USCAR-2 5.1.8的规定，用目视法检查产品外观。\n2、目视和RAL色卡对比。",
            "test_criteria": "1）端子无变形、断裂、锈蚀、残缺等不良缺陷；\n2）任何锁止、卡点结构安装后无脱落、无断裂等不良缺陷；\n3）橡胶密封件的表面应该光滑、色泽均匀，无飞边、毛刺、欠硫变形、起泡、裂口、杂质、喷霜、皱皮等不良现象；\n4）金属材质的壳体、插座的安装面板及屏蔽环等金属部件应无毛刺、尖锐角、裂痕、脱层、生锈、镀层脱落等不良现象；\n5）塑料材质的壳体、插座的安装面板等非金属部件应无变形、纹路、开裂、起泡、划痕、杂质等不良现象；\n6）键位A主体塑料部分颜色应该为黑色RAL 9004、可接受值\n      键位B主体塑料部分颜色应该为橙色RAL 2003、可接受值RAL2004、RAL2008\n      键位C主体塑料部分颜色应该为蓝色RAL5017、可接受值\n      键位D主体塑料部分颜色应该为灰色RAL7004、可接受值",
            "sample_quantity": "4套"
        },
        {
            "test_name": "Connector and/or Terminal Cycling",
            "test_name_cn": "连接器或者端子循环",
            "test_spec": "按SAE/USCAR-2 5.1.7的规定。本程序是连接器或端子对在接受一系列测试前的预处理，插拔次数：10次",
            "test_criteria": "连接器或端子对能够可靠插拔，无异常。",
            "sample_quantity": None
        },
        {
            "test_name": "Insulation Resistance",
            "test_name_cn": "绝缘电阻",
            "test_spec": "按SAE/USCAR-2 5.5.1的规定。",
            "test_criteria": "端子与相邻孔位端子/外壳金属镶件之间的绝缘电阻≥100MΩ",
            "sample_quantity": None
        },
        {
            "test_name": "Pressure/Vacuum Leak",
            "test_name_cn": "压力/真空泄露",
            "test_spec": "按SAE/USCAR-2 5.6.6的规定，执行5.6.6.3第1-9测试步骤，测试气压±48kPa。",
            "test_criteria": "1、试验过程中，连接器不应有气泡冒出，内部目视无水分；\n2、满足后续实验要求",
            "sample_quantity": None
        },
        {
            "test_name": "Insulation Resistance",
            "test_name_cn": "绝缘电阻",
            "test_spec": "按SAE/USCAR-2 5.5.1的规定。",
            "test_criteria": "端子与相邻孔位端子/外壳金属镶件之间的绝缘电阻≥100MΩ",
            "sample_quantity": None
        },
        {
            "test_name": "Degree-of-protection test",
            "test_name_cn": "防护等级测试",
            "test_spec": "按GB/T 30038 中第 8 章的规定。\n防护等级：IPX8（1m 水深 24h）",
            "test_criteria": "试验后，连接器内部目视无水分，且能满足后续试验要求；",
            "sample_quantity": None
        },
        {
            "test_name": "Insulation Resistance",
            "test_name_cn": "绝缘电阻",
            "test_spec": "按SAE/USCAR-2 5.5.1的规定。",
            "test_criteria": "端子与相邻孔位端子/外壳金属镶件之间的绝缘电阻≥100MΩ",
            "sample_quantity": None
        },
        {
            "test_name": "Dielectric withstand voltage test",
            "test_name_cn": "耐压测试",
            "test_spec": "按SAE/USCAR-37 5.5.2的规定，并符合如下细则：\n测试电压：1600V DC ",
            "test_criteria": "端子与端子/外壳金属镶件之间无飞弧或击穿现象，电流泄漏≤5mA",
            "sample_quantity": None
        },
        {
            "test_name": "Visual Inspection",
            "test_name_cn": "外观检查",
            "test_spec": "按SAE/USCAR-2 5.1.8的规定，用目视法检查产品外观。",
            "test_criteria": "1）端子无变形、断裂、锈蚀、残缺等不良缺陷；\n2）任何锁止、卡点结构安装后无脱落、无断裂等不良缺陷；\n3）橡胶密封件的表面应该光滑、色泽均匀，无飞边、毛刺、欠硫变形、起泡、裂口、杂质、喷霜、皱皮等不良现象；\n4）金属材质的壳体、插座的安装面板及屏蔽环等金属部件应无毛刺、尖锐角、裂痕、脱层、生锈、镀层脱落等不良现象；\n5）塑料材质的壳体、插座的安装面板等非金属部件应无变形、纹路、开裂、起泡、划痕、杂质等不良现象；\n6）键位A主体塑料部分颜色应该为黑色RAL 9004、可接受值\n      键位B主体塑料部分颜色应该为橙色RAL 2003、可接受值RAL2004、RAL2008\n      键位C主体塑料部分颜色应该为蓝色RAL5017、可接受值\n      键位D主体塑料部分颜色应该为灰色RAL7004、可接受值",
            "sample_quantity": None
        }
    ]

        # Populate the database with test items
    for item in test_items:
            test_item = TestItemBaseInfo(
                test_name=item["test_name"],
                test_name_cn=item["test_name_cn"],
                test_spec=item["test_spec"],
                test_criteria=item["test_criteria"],
                sample_quantity=item["sample_quantity"]
            )
            db.session.add(test_item)

        # Commit the changes to the database
    db.session.commit()
    print(f"Successfully populated {len(test_items)} test items.")