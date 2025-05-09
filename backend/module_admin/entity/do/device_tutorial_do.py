from sqlalchemy import Integer, DateTime, Column, CHAR, String
from config.database import Base


class SysDeviceTutorial(Base):
    """
    仪器教程表
    """

    __tablename__ = 'sys_device_tutorial'

    tutorial_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='教程ID')
    device_id = Column(Integer, nullable=True, comment='仪器ID')
    tutorial_title = Column(String(30), nullable=False, comment='教程标题')
    tutorial_category = Column(CHAR(1), nullable=True, comment='教程类别(0文本 1视频)')
    tutorial_file = Column(String(200), nullable=True, comment='本地文件')
    tutorial_url = Column(String(200), nullable=True, comment='外部链接')
    create_by = Column(String(30), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



