from sqlalchemy import Column, DateTime, Integer, String, Text
from config.database import Base


class SysRefArticle(Base):
    """
    文献分析表
    """

    __tablename__ = 'sys_ref_article'

    article_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='文章id')
    article_name = Column(String(80), nullable=False, comment='文章名称')
    ref_id = Column(Integer, nullable=False, comment='文献id')
    article_content = Column(Text, nullable=True, comment='文章内容')
    create_by = Column(String(30), nullable=True, comment='创建人')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(30), nullable=True, comment='更新人')
    update_time = Column(DateTime, nullable=True, comment='更新时间')



