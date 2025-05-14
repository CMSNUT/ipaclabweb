from sqlalchemy import Integer, Column
from config.database import Base


class SysDatasetTag(Base):
    """
    数据与标签关联表
    """

    __tablename__ = 'sys_dataset_tag'

    dataset_id = Column(Integer, primary_key=True, nullable=False, comment='数据ID')
    tag_id = Column(Integer, primary_key=True, nullable=False, comment='标签ID')



