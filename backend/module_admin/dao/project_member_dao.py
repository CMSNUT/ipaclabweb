from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.project_member_do import SysProjectMember
from module_admin.entity.vo.project_member_vo import Project_memberModel, Project_memberPageQueryModel
from utils.page_util import PageUtil


class Project_memberDao:
    """
    项目与用户关联模块数据库操作层
    """

    @classmethod
    async def get_project_member_detail_by_id(cls, db: AsyncSession, project_id: int):
        """
        根据数据ID获取项目与用户关联详细信息

        :param db: orm对象
        :param project_id: 数据ID
        :return: 项目与用户关联信息对象
        """
        project_member_info = (
            (
                await db.execute(
                    select(SysProjectMember)
                    .where(
                        SysProjectMember.project_id == project_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_member_info

    @classmethod
    async def get_project_member_detail_by_info(cls, db: AsyncSession, project_member: Project_memberModel):
        """
        根据项目与用户关联参数获取项目与用户关联信息

        :param db: orm对象
        :param project_member: 项目与用户关联参数对象
        :return: 项目与用户关联信息对象
        """
        project_member_info = (
            (
                await db.execute(
                    select(SysProjectMember).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_member_info

    @classmethod
    async def get_project_member_list(cls, db: AsyncSession, query_object: Project_memberPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取项目与用户关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目与用户关联列表信息对象
        """
        query = (
            select(SysProjectMember)
            .where(
                SysProjectMember.member_role == query_object.member_role if query_object.member_role else True,
            )
            .order_by(SysProjectMember.project_id)
            .distinct()
        )
        project_member_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return project_member_list

    @classmethod
    async def add_project_member_dao(cls, db: AsyncSession, project_member: Project_memberModel):
        """
        新增项目与用户关联数据库操作

        :param db: orm对象
        :param project_member: 项目与用户关联对象
        :return:
        """
        db_project_member = SysProjectMember(**project_member.model_dump(exclude={}))
        db.add(db_project_member)
        await db.flush()

        return db_project_member

    @classmethod
    async def edit_project_member_dao(cls, db: AsyncSession, project_member: dict):
        """
        编辑项目与用户关联数据库操作

        :param db: orm对象
        :param project_member: 需要更新的项目与用户关联字典
        :return:
        """
        await db.execute(update(SysProjectMember), [project_member])

    @classmethod
    async def delete_project_member_dao(cls, db: AsyncSession, project_member: Project_memberModel):
        """
        删除项目与用户关联数据库操作

        :param db: orm对象
        :param project_member: 项目与用户关联对象
        :return:
        """
        await db.execute(delete(SysProjectMember).where(SysProjectMember.project_id.in_([project_member.project_id])))

