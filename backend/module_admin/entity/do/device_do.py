from sqlalchemy import Column, String, DateTime, Integer
from config.database import Base


class SysDevice(Base):
    """
    仪器管理表
    """

    __tablename__ = 'sys_device'

    device_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='仪器id')
    device_name = Column(String(50), nullable=False, comment='仪器名称')
    device_img = Column(String(100), nullable=True, comment='仪器图片地址')
    device_desc = Column(String(512), nullable=True, comment='仪器简介')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



