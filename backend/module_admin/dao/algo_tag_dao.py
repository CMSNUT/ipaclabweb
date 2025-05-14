from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.algo_tag_do import SysAlgoTag
from module_admin.entity.vo.algo_tag_vo import Algo_tagModel, Algo_tagPageQueryModel
from utils.page_util import PageUtil


class Algo_tagDao:
    """
    算法与标签关联模块数据库操作层
    """

    @classmethod
    async def get_algo_tag_detail_by_id(cls, db: AsyncSession, algo_id: int):
        """
        根据算法ID获取算法与标签关联详细信息

        :param db: orm对象
        :param algo_id: 算法ID
        :return: 算法与标签关联信息对象
        """
        algo_tag_info = (
            (
                await db.execute(
                    select(SysAlgoTag)
                    .where(
                        SysAlgoTag.algo_id == algo_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return algo_tag_info

    @classmethod
    async def get_algo_tag_detail_by_info(cls, db: AsyncSession, algo_tag: Algo_tagModel):
        """
        根据算法与标签关联参数获取算法与标签关联信息

        :param db: orm对象
        :param algo_tag: 算法与标签关联参数对象
        :return: 算法与标签关联信息对象
        """
        algo_tag_info = (
            (
                await db.execute(
                    select(SysAlgoTag).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return algo_tag_info

    @classmethod
    async def get_algo_tag_list(cls, db: AsyncSession, query_object: Algo_tagPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取算法与标签关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 算法与标签关联列表信息对象
        """
        query = (
            select(SysAlgoTag)
            .where(
            )
            .order_by(SysAlgoTag.algo_id)
            .distinct()
        )
        algo_tag_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return algo_tag_list

    @classmethod
    async def add_algo_tag_dao(cls, db: AsyncSession, algo_tag: Algo_tagModel):
        """
        新增算法与标签关联数据库操作

        :param db: orm对象
        :param algo_tag: 算法与标签关联对象
        :return:
        """
        db_algo_tag = SysAlgoTag(**algo_tag.model_dump(exclude={}))
        db.add(db_algo_tag)
        await db.flush()

        return db_algo_tag

    @classmethod
    async def edit_algo_tag_dao(cls, db: AsyncSession, algo_tag: dict):
        """
        编辑算法与标签关联数据库操作

        :param db: orm对象
        :param algo_tag: 需要更新的算法与标签关联字典
        :return:
        """
        await db.execute(update(SysAlgoTag), [algo_tag])

    @classmethod
    async def delete_algo_tag_dao(cls, db: AsyncSession, algo_tag: Algo_tagModel):
        """
        删除算法与标签关联数据库操作

        :param db: orm对象
        :param algo_tag: 算法与标签关联对象
        :return:
        """
        await db.execute(delete(SysAlgoTag).where(SysAlgoTag.algo_id.in_([algo_tag.algo_id])))

