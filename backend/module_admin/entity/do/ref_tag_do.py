from sqlalchemy import Integer, Column
from config.database import Base


class SysRefTag(Base):
    """
    文献与标签关联表
    """

    __tablename__ = 'sys_ref_tag'

    ref_id = Column(Integer, primary_key=True, nullable=False, comment='文献ID')
    tag_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')



