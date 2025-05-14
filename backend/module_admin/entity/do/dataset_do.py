from sqlalchemy import DateTime, String, Column, Text, Integer
from config.database import Base


class SysDataset(Base):
    """
    数据管理表
    """

    __tablename__ = 'sys_dataset'

    dataset_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='数据id')
    dataset_name = Column(String(80), nullable=False, comment='数据名称')
    dataset_desc = Column(String(200), nullable=True, comment='数据简介')
    dataset_content = Column(Text, nullable=True, comment='数据详情')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



