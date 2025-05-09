from sqlalchemy import DateTime, Integer, Column, String
from config.database import Base


class SysDevice(Base):
    """
    仪器信息表
    """

    __tablename__ = 'sys_device'

    device_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='仪器ID')
    device_name = Column(String(30), nullable=False, comment='仪器名称')
    device_model = Column(String(30), nullable=True, comment='仪器型号')
    device_remark = Column(String(200), nullable=True, comment='功能简介')
    device_room = Column(String(20), nullable=True, comment='存放位置')
    device_img = Column(String(200), nullable=True, comment='图片地址')
    create_by = Column(String(30), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



