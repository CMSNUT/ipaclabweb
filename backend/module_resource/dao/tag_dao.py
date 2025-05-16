from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_resource.entity.do.tag_do import ResTag
from module_resource.entity.vo.tag_vo import TagModel, TagPageQueryModel
from utils.page_util import PageUtil


class TagDao:
    """
    标签管理模块数据库操作层
    """

    @classmethod
    async def get_tag_detail_by_id(cls, db: AsyncSession, tag_id: int):
        """
        根据标签id获取标签管理详细信息

        :param db: orm对象
        :param tag_id: 标签id
        :return: 标签管理信息对象
        """
        tag_info = (
            (
                await db.execute(
                    select(ResTag)
                    .where(
                        ResTag.tag_id == tag_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return tag_info

    @classmethod
    async def get_tag_detail_by_info(cls, db: AsyncSession, tag: TagModel):
        """
        根据标签管理参数获取标签管理信息

        :param db: orm对象
        :param tag: 标签管理参数对象
        :return: 标签管理信息对象
        """
        tag_info = (
            (
                await db.execute(
                    select(ResTag).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return tag_info

    @classmethod
    async def get_tag_list(cls, db: AsyncSession, query_object: TagPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取标签管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标签管理列表信息对象
        """
        query = (
            select(ResTag)
            .where(
                ResTag.tag_name.like(f'%{query_object.tag_name}%') if query_object.tag_name else True,
            )
            .order_by(ResTag.tag_id)
            .distinct()
        )
        tag_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return tag_list

    @classmethod
    async def add_tag_dao(cls, db: AsyncSession, tag: TagModel):
        """
        新增标签管理数据库操作

        :param db: orm对象
        :param tag: 标签管理对象
        :return:
        """
        db_tag = ResTag(**tag.model_dump(exclude={}))
        db.add(db_tag)
        await db.flush()

        return db_tag

    @classmethod
    async def edit_tag_dao(cls, db: AsyncSession, tag: dict):
        """
        编辑标签管理数据库操作

        :param db: orm对象
        :param tag: 需要更新的标签管理字典
        :return:
        """
        await db.execute(update(ResTag), [tag])

    @classmethod
    async def delete_tag_dao(cls, db: AsyncSession, tag: TagModel):
        """
        删除标签管理数据库操作

        :param db: orm对象
        :param tag: 标签管理对象
        :return:
        """
        await db.execute(delete(ResTag).where(ResTag.tag_id.in_([tag.tag_id])))

