from sqlalchemy import Column, Integer
from config.database import Base


class SysAlgoTag(Base):
    """
    算法与标签关联表
    """

    __tablename__ = 'sys_algo_tag'

    algo_id = Column(Integer, primary_key=True, nullable=False, comment='算法ID')
    tag_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')



