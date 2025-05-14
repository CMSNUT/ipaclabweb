from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.ref_tag_do import SysRefTag
from module_admin.entity.vo.ref_tag_vo import Ref_tagModel, Ref_tagPageQueryModel
from utils.page_util import PageUtil


class Ref_tagDao:
    """
    文献与标签关联模块数据库操作层
    """

    @classmethod
    async def get_ref_tag_detail_by_id(cls, db: AsyncSession, ref_id: int):
        """
        根据文献ID获取文献与标签关联详细信息

        :param db: orm对象
        :param ref_id: 文献ID
        :return: 文献与标签关联信息对象
        """
        ref_tag_info = (
            (
                await db.execute(
                    select(SysRefTag)
                    .where(
                        SysRefTag.ref_id == ref_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_tag_info

    @classmethod
    async def get_ref_tag_detail_by_info(cls, db: AsyncSession, ref_tag: Ref_tagModel):
        """
        根据文献与标签关联参数获取文献与标签关联信息

        :param db: orm对象
        :param ref_tag: 文献与标签关联参数对象
        :return: 文献与标签关联信息对象
        """
        ref_tag_info = (
            (
                await db.execute(
                    select(SysRefTag).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_tag_info

    @classmethod
    async def get_ref_tag_list(cls, db: AsyncSession, query_object: Ref_tagPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取文献与标签关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献与标签关联列表信息对象
        """
        query = (
            select(SysRefTag)
            .where(
            )
            .order_by(SysRefTag.ref_id)
            .distinct()
        )
        ref_tag_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return ref_tag_list

    @classmethod
    async def add_ref_tag_dao(cls, db: AsyncSession, ref_tag: Ref_tagModel):
        """
        新增文献与标签关联数据库操作

        :param db: orm对象
        :param ref_tag: 文献与标签关联对象
        :return:
        """
        db_ref_tag = SysRefTag(**ref_tag.model_dump(exclude={}))
        db.add(db_ref_tag)
        await db.flush()

        return db_ref_tag

    @classmethod
    async def edit_ref_tag_dao(cls, db: AsyncSession, ref_tag: dict):
        """
        编辑文献与标签关联数据库操作

        :param db: orm对象
        :param ref_tag: 需要更新的文献与标签关联字典
        :return:
        """
        await db.execute(update(SysRefTag), [ref_tag])

    @classmethod
    async def delete_ref_tag_dao(cls, db: AsyncSession, ref_tag: Ref_tagModel):
        """
        删除文献与标签关联数据库操作

        :param db: orm对象
        :param ref_tag: 文献与标签关联对象
        :return:
        """
        await db.execute(delete(SysRefTag).where(SysRefTag.ref_id.in_([ref_tag.ref_id])))

