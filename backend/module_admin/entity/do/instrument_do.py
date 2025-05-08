from sqlalchemy import DateTime, Integer, String, Column
from config.database import Base


class SysInstrument(Base):
    """
    仪器信息表
    """

    __tablename__ = 'sys_instrument'

    instrument_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='仪器ID')
    instrument_name = Column(String(30), nullable=False, comment='仪器名称')
    instrument_model = Column(String(30), nullable=True, comment='仪器型号')
    instrument_remark = Column(String(200), nullable=True, comment='功能简介')
    instrument_room = Column(String(20), nullable=True, comment='存放位置')
    instrument_img = Column(String(200), nullable=True, comment='图片地址')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



