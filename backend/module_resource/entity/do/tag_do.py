from sqlalchemy import Integer, Column, DateTime, String
from config.database import Base


class ResTag(Base):
    """
    标签管理表
    """

    __tablename__ = 'res_tag'

    tag_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='标签id')
    tag_label = Column(String(20), nullable=False, comment='标签名称')
    tag_value = Column(String(20), nullable=False, comment='标签值')
    parent_id = Column(Integer, nullable=True, comment='父标签id')
    create_by = Column(String(15), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(15), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



