
from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey,String,Integer,Text,Boolean, DateTime,BigInteger, Unicode
from .basemodel import BasicMode
from src.core.extensions import db
#from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey,String,Integer,Text,Boolean, DateTime,BigInteger, Unicode, Date
from .basemodel import BasicMode



class Device(db.Model,BasicMode):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='序号')
    manage_code = Column(Unicode(50), comment='管理编号')
    device_type = Column(Unicode(100), comment='设备类型')
    device_name = Column(Unicode(100), comment='设备名称')
    device_model = Column(Unicode(100), comment='设备型号')
    serial_number = Column(Unicode(100), comment='出厂编号')
    manufacturer = Column(Unicode(100), comment='制造厂商')
    management_department = Column(Unicode(100), comment='管理部门')
    location = Column(Unicode(100), comment='放置位置')
    start_date = Column(Date, comment='起用时间')
    check_cycle = Column(Unicode(50), comment='校准/检查周期')
    last_check_date = Column(Date, comment='最近检定/完好评定日期')
    status = Column(Unicode(50), comment='使用状态')
    check_type = Column(Unicode(100), comment='计量校准/完好评定')
    next_check_date = Column(Date, comment='有效期/下次检查日期')
    metering_property = Column(Unicode(100), comment='计量特性')
    unit = Column(Unicode(50), comment='计量单位')
    remarks = Column(Text, comment='备注')
    __field_name_map = {
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