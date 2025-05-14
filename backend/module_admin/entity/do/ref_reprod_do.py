from sqlalchemy import Column, DateTime, Integer, String, Text
from config.database import Base


class SysRefReprod(Base):
    """
    文献复现表
    """

    __tablename__ = 'sys_ref_reprod'

    reprod_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='复现id')
    reprod_name = Column(String(80), nullable=False, comment='复现名称')
    ref_id = Column(Integer, nullable=False, comment='文献id')
    reprod_content = Column(Text, nullable=True, comment='复现内容')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



