from sqlalchemy import Integer, Column
from config.database import Base


class ResAlgoTag(Base):
    """
    算法与标签关联表
    """

    __tablename__ = 'res_algo_tag'

    algo_id = Column(Integer, primary_key=True, nullable=False, comment='算法ID')
    tag_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')



