from sqlalchemy import DateTime, Column, Integer, String
from config.database import Base


class ResDevice(Base):
    """
    仪器管理表
    """

    __tablename__ = 'res_device'

    device_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='仪器ID')
    device_name = Column(String(64), nullable=False, comment='仪器名称')
    device_img = Column(String(100), nullable=True, comment='仪器图片')
    create_by = Column(String(15), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(15), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



