from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.project_tag_do import SysProjectTag
from module_admin.entity.vo.project_tag_vo import Project_tagModel, Project_tagPageQueryModel
from utils.page_util import PageUtil


class Project_tagDao:
    """
    数据与标签关联模块数据库操作层
    """

    @classmethod
    async def get_project_tag_detail_by_id(cls, db: AsyncSession, project_id: int):
        """
        根据项目ID获取数据与标签关联详细信息

        :param db: orm对象
        :param project_id: 项目ID
        :return: 数据与标签关联信息对象
        """
        project_tag_info = (
            (
                await db.execute(
                    select(SysProjectTag)
                    .where(
                        SysProjectTag.project_id == project_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_tag_info

    @classmethod
    async def get_project_tag_detail_by_info(cls, db: AsyncSession, project_tag: Project_tagModel):
        """
        根据数据与标签关联参数获取数据与标签关联信息

        :param db: orm对象
        :param project_tag: 数据与标签关联参数对象
        :return: 数据与标签关联信息对象
        """
        project_tag_info = (
            (
                await db.execute(
                    select(SysProjectTag).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_tag_info

    @classmethod
    async def get_project_tag_list(cls, db: AsyncSession, query_object: Project_tagPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取数据与标签关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据与标签关联列表信息对象
        """
        query = (
            select(SysProjectTag)
            .where(
            )
            .order_by(SysProjectTag.project_id)
            .distinct()
        )
        project_tag_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return project_tag_list

    @classmethod
    async def add_project_tag_dao(cls, db: AsyncSession, project_tag: Project_tagModel):
        """
        新增数据与标签关联数据库操作

        :param db: orm对象
        :param project_tag: 数据与标签关联对象
        :return:
        """
        db_project_tag = SysProjectTag(**project_tag.model_dump(exclude={}))
        db.add(db_project_tag)
        await db.flush()

        return db_project_tag

    @classmethod
    async def edit_project_tag_dao(cls, db: AsyncSession, project_tag: dict):
        """
        编辑数据与标签关联数据库操作

        :param db: orm对象
        :param project_tag: 需要更新的数据与标签关联字典
        :return:
        """
        await db.execute(update(SysProjectTag), [project_tag])

    @classmethod
    async def delete_project_tag_dao(cls, db: AsyncSession, project_tag: Project_tagModel):
        """
        删除数据与标签关联数据库操作

        :param db: orm对象
        :param project_tag: 数据与标签关联对象
        :return:
        """
        await db.execute(delete(SysProjectTag).where(SysProjectTag.project_id.in_([project_tag.project_id])))

