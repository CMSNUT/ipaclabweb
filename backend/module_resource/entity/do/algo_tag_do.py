from sqlalchemy import DateTime, String, Integer, Column
from config.database import Base


class ResAlgoTag(Base):
    """
    程序标签关联表
    """

    __tablename__ = 'res_algo_tag'

    algo_id = Column(Integer, primary_key=True, nullable=False, comment='程序ID')
    tag_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')
    create_by = Column(String(15), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(15), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



