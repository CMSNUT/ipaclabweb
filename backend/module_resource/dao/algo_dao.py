from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_resource.entity.do.algo_do import ResAlgo
from module_resource.entity.vo.algo_vo import AlgoModel, AlgoPageQueryModel
from utils.page_util import PageUtil


class AlgoDao:
    """
    算法管理模块数据库操作层
    """

    @classmethod
    async def get_algo_detail_by_id(cls, db: AsyncSession, algo_id: int):
        """
        根据算法id获取算法管理详细信息

        :param db: orm对象
        :param algo_id: 算法id
        :return: 算法管理信息对象
        """
        algo_info = (
            (
                await db.execute(
                    select(ResAlgo)
                    .where(
                        ResAlgo.algo_id == algo_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return algo_info

    @classmethod
    async def get_algo_detail_by_info(cls, db: AsyncSession, algo: AlgoModel):
        """
        根据算法管理参数获取算法管理信息

        :param db: orm对象
        :param algo: 算法管理参数对象
        :return: 算法管理信息对象
        """
        algo_info = (
            (
                await db.execute(
                    select(ResAlgo).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return algo_info

    @classmethod
    async def get_algo_list(cls, db: AsyncSession, query_object: AlgoPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取算法管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 算法管理列表信息对象
        """
        query = (
            select(ResAlgo)
            .where(
                ResAlgo.algo_name.like(f'%{query_object.algo_name}%') if query_object.algo_name else True,
                ResAlgo.algo_type == query_object.algo_type if query_object.algo_type else True,
                ResAlgo.algo_lang == query_object.algo_lang if query_object.algo_lang else True,
            )
            .order_by(ResAlgo.algo_id)
            .distinct()
        )
        algo_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return algo_list

    @classmethod
    async def add_algo_dao(cls, db: AsyncSession, algo: AlgoModel):
        """
        新增算法管理数据库操作

        :param db: orm对象
        :param algo: 算法管理对象
        :return:
        """
        db_algo = ResAlgo(**algo.model_dump(exclude={}))
        db.add(db_algo)
        await db.flush()

        return db_algo

    @classmethod
    async def edit_algo_dao(cls, db: AsyncSession, algo: dict):
        """
        编辑算法管理数据库操作

        :param db: orm对象
        :param algo: 需要更新的算法管理字典
        :return:
        """
        await db.execute(update(ResAlgo), [algo])

    @classmethod
    async def delete_algo_dao(cls, db: AsyncSession, algo: AlgoModel):
        """
        删除算法管理数据库操作

        :param db: orm对象
        :param algo: 算法管理对象
        :return:
        """
        await db.execute(delete(ResAlgo).where(ResAlgo.algo_id.in_([algo.algo_id])))

