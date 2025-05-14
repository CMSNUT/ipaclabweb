from sqlalchemy import Column, DateTime, Integer, String, Text
from config.database import Base


class SysProjectDoc(Base):
    """
    项目文档表
    """

    __tablename__ = 'sys_project_doc'

    doc_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='文档id')
    doc_name = Column(String(80), nullable=False, comment='文档名称')
    project_id = Column(Integer, nullable=False, comment='文献id')
    doc_desc = Column(String(200), nullable=False, comment='文档简介')
    doc_content = Column(Text, nullable=True, comment='文档内容')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



