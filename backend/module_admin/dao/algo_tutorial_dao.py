from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.algo_tutorial_do import SysAlgoTutorial
from module_admin.entity.vo.algo_tutorial_vo import Algo_tutorialModel, Algo_tutorialPageQueryModel
from utils.page_util import PageUtil


class Algo_tutorialDao:
    """
    算法教程模块数据库操作层
    """

    @classmethod
    async def get_algo_tutorial_detail_by_id(cls, db: AsyncSession, tutorial_id: int):
        """
        根据教程id获取算法教程详细信息

        :param db: orm对象
        :param tutorial_id: 教程id
        :return: 算法教程信息对象
        """
        algo_tutorial_info = (
            (
                await db.execute(
                    select(SysAlgoTutorial)
                    .where(
                        SysAlgoTutorial.tutorial_id == tutorial_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return algo_tutorial_info

    @classmethod
    async def get_algo_tutorial_detail_by_info(cls, db: AsyncSession, algo_tutorial: Algo_tutorialModel):
        """
        根据算法教程参数获取算法教程信息

        :param db: orm对象
        :param algo_tutorial: 算法教程参数对象
        :return: 算法教程信息对象
        """
        algo_tutorial_info = (
            (
                await db.execute(
                    select(SysAlgoTutorial).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return algo_tutorial_info

    @classmethod
    async def get_algo_tutorial_list(cls, db: AsyncSession, query_object: Algo_tutorialPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取算法教程列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 算法教程列表信息对象
        """
        query = (
            select(SysAlgoTutorial)
            .where(
                SysAlgoTutorial.tutorial_name.like(f'%{query_object.tutorial_name}%') if query_object.tutorial_name else True,
                SysAlgoTutorial.algo_id == query_object.algo_id if query_object.algo_id else True,
                SysAlgoTutorial.tutorial_content.like(f'%{query_object.tutorial_content}%') if query_object.tutorial_content else True,
            )
            .order_by(SysAlgoTutorial.tutorial_id)
            .distinct()
        )
        algo_tutorial_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return algo_tutorial_list

    @classmethod
    async def add_algo_tutorial_dao(cls, db: AsyncSession, algo_tutorial: Algo_tutorialModel):
        """
        新增算法教程数据库操作

        :param db: orm对象
        :param algo_tutorial: 算法教程对象
        :return:
        """
        db_algo_tutorial = SysAlgoTutorial(**algo_tutorial.model_dump(exclude={}))
        db.add(db_algo_tutorial)
        await db.flush()

        return db_algo_tutorial

    @classmethod
    async def edit_algo_tutorial_dao(cls, db: AsyncSession, algo_tutorial: dict):
        """
        编辑算法教程数据库操作

        :param db: orm对象
        :param algo_tutorial: 需要更新的算法教程字典
        :return:
        """
        await db.execute(update(SysAlgoTutorial), [algo_tutorial])

    @classmethod
    async def delete_algo_tutorial_dao(cls, db: AsyncSession, algo_tutorial: Algo_tutorialModel):
        """
        删除算法教程数据库操作

        :param db: orm对象
        :param algo_tutorial: 算法教程对象
        :return:
        """
        await db.execute(delete(SysAlgoTutorial).where(SysAlgoTutorial.tutorial_id.in_([algo_tutorial.tutorial_id])))

