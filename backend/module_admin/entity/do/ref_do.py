from sqlalchemy import Column, DateTime, Integer, String, Text
from config.database import Base


class SysRef(Base):
    """
    文献管理表
    """

    __tablename__ = 'sys_ref'

    ref_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='文献id')
    ref_title = Column(Text, nullable=False, comment='文献英文标题')
    ref_title_zh = Column(Text, nullable=True, comment='文献中文标题')
    ref_doi = Column(Text, nullable=True, comment='文献DOI')
    ref_abs = Column(Text, nullable=True, comment='文献摘要')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



