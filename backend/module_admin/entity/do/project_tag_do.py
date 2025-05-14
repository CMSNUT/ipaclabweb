from sqlalchemy import Column, Integer
from config.database import Base


class SysProjectTag(Base):
    """
    数据与标签关联表
    """

    __tablename__ = 'sys_project_tag'

    project_id = Column(Integer, primary_key=True, nullable=False, comment='项目ID')
    tag_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')



