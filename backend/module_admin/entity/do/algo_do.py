from sqlalchemy import Column, DateTime, CHAR, Integer, String, Text
from config.database import Base


class SysAlgo(Base):
    """
    算法管理表
    """

    __tablename__ = 'sys_algo'

    algo_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='算法id')
    algo_name = Column(String(80), nullable=False, comment='算法名称')
    algo_type = Column(CHAR(1), nullable=True, comment='算法类别')
    algo_lang = Column(CHAR(1), nullable=True, comment='算法语言')
    algo_content = Column(Text, nullable=True, comment='算法详情')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



