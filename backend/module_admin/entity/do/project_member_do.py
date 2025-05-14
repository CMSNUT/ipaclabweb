from sqlalchemy import String, Column, BigInteger, Integer
from config.database import Base


class SysProjectMember(Base):
    """
    项目与用户关联表
    """

    __tablename__ = 'sys_project_member'

    project_id = Column(Integer, primary_key=True, nullable=False, comment='数据ID')
    user_id = Column(BigInteger, primary_key=True, nullable=False, comment='标签ID')
    member_role = Column(String(200), nullable=True, comment='项目分工')



