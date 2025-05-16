from sqlalchemy import String, DateTime, Text, Integer, Column, CHAR
from config.database import Base


class ResAlgo(Base):
    """
    程序管理表
    """

    __tablename__ = 'res_algo'

    algo_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='程序ID')
    algo_name = Column(String(64), nullable=False, comment='程序名称')
    algo_desc = Column(Text, nullable=True, comment='程序介绍')
    algo_type = Column(CHAR(1), nullable=False, comment='程序类型')
    algo_lang = Column(CHAR(1), nullable=False, comment='编程语言')
    create_by = Column(String(15), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(15), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



