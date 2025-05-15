from sqlalchemy import Integer, Column, String
from config.database import Base


class SysTag(Base):
    """
    标签管理表
    """

    __tablename__ = 'sys_tag'

    tag_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='标签id')
    tag_name = Column(String(20), nullable=False, comment='标签名称')



