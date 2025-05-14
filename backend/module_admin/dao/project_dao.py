from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.project_do import SysProject
from module_admin.entity.vo.project_vo import ProjectModel, ProjectPageQueryModel
from utils.page_util import PageUtil


class ProjectDao:
    """
    项目管理模块数据库操作层
    """

    @classmethod
    async def get_project_detail_by_id(cls, db: AsyncSession, project_id: int):
        """
        根据项目id获取项目管理详细信息

        :param db: orm对象
        :param project_id: 项目id
        :return: 项目管理信息对象
        """
        project_info = (
            (
                await db.execute(
                    select(SysProject)
                    .where(
                        SysProject.project_id == project_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_info

    @classmethod
    async def get_project_detail_by_info(cls, db: AsyncSession, project: ProjectModel):
        """
        根据项目管理参数获取项目管理信息

        :param db: orm对象
        :param project: 项目管理参数对象
        :return: 项目管理信息对象
        """
        project_info = (
            (
                await db.execute(
                    select(SysProject).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_info

    @classmethod
    async def get_project_list(cls, db: AsyncSession, query_object: ProjectPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取项目管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目管理列表信息对象
        """
        query = (
            select(SysProject)
            .where(
                SysProject.project_title == query_object.project_title if query_object.project_title else True,
                SysProject.user_id == query_object.user_id if query_object.user_id else True,
                SysProject.project_desc.like(f'%{query_object.project_desc}%') if query_object.project_desc else True,
            )
            .order_by(SysProject.project_id)
            .distinct()
        )
        project_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return project_list

    @classmethod
    async def add_project_dao(cls, db: AsyncSession, project: ProjectModel):
        """
        新增项目管理数据库操作

        :param db: orm对象
        :param project: 项目管理对象
        :return:
        """
        db_project = SysProject(**project.model_dump(exclude={}))
        db.add(db_project)
        await db.flush()

        return db_project

    @classmethod
    async def edit_project_dao(cls, db: AsyncSession, project: dict):
        """
        编辑项目管理数据库操作

        :param db: orm对象
        :param project: 需要更新的项目管理字典
        :return:
        """
        await db.execute(update(SysProject), [project])

    @classmethod
    async def delete_project_dao(cls, db: AsyncSession, project: ProjectModel):
        """
        删除项目管理数据库操作

        :param db: orm对象
        :param project: 项目管理对象
        :return:
        """
        await db.execute(delete(SysProject).where(SysProject.project_id.in_([project.project_id])))

