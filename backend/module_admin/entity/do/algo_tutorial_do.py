from sqlalchemy import Column, DateTime, Integer, String, Text
from config.database import Base


class SysAlgoTutorial(Base):
    """
    算法教程表
    """

    __tablename__ = 'sys_algo_tutorial'

    tutorial_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='教程id')
    tutorial_name = Column(String(80), nullable=False, comment='教程名称')
    algo_id = Column(Integer, nullable=False, comment='算法id')
    tutorial_content = Column(Text, nullable=True, comment='教程内容')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



