from sqlalchemy import Column, DateTime, Integer, String, BigInteger, Text
from config.database import Base


class SysProject(Base):
    """
    项目管理表
    """

    __tablename__ = 'sys_project'

    project_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='项目id')
    project_title = Column(String(40), nullable=False, comment='项目标题')
    user_id = Column(BigInteger, nullable=False, comment='项目负责人')
    project_desc = Column(Text, nullable=True, comment='项目描述')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



