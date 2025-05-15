from sqlalchemy import Integer, DateTime, Column, String
from config.database import Base


class ResDevice(Base):
    """
    仪器管理表
    """

    __tablename__ = 'res_device'

    device_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='仪器id')
    device_name = Column(String(50), nullable=False, comment='仪器名称')
    device_img = Column(String(100), nullable=True, comment='图片地址')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



