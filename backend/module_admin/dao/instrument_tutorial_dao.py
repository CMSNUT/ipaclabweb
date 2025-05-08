from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.instrument_tutorial_do import SysInstrumentTutorial
from module_admin.entity.vo.instrument_tutorial_vo import Instrument_tutorialModel, Instrument_tutorialPageQueryModel
from utils.page_util import PageUtil


class Instrument_tutorialDao:
    """
    仪器教程模块数据库操作层
    """

    @classmethod
    async def get_instrument_tutorial_detail_by_id(cls, db: AsyncSession, tutorial_id: int):
        """
        根据教程ID获取仪器教程详细信息

        :param db: orm对象
        :param tutorial_id: 教程ID
        :return: 仪器教程信息对象
        """
        instrument_tutorial_info = (
            (
                await db.execute(
                    select(SysInstrumentTutorial)
                    .where(
                        SysInstrumentTutorial.tutorial_id == tutorial_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return instrument_tutorial_info

    @classmethod
    async def get_instrument_tutorial_detail_by_info(cls, db: AsyncSession, instrument_tutorial: Instrument_tutorialModel):
        """
        根据仪器教程参数获取仪器教程信息

        :param db: orm对象
        :param instrument_tutorial: 仪器教程参数对象
        :return: 仪器教程信息对象
        """
        instrument_tutorial_info = (
            (
                await db.execute(
                    select(SysInstrumentTutorial).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return instrument_tutorial_info

    @classmethod
    async def get_instrument_tutorial_list(cls, db: AsyncSession, query_object: Instrument_tutorialPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取仪器教程列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器教程列表信息对象
        """
        query = (
            select(SysInstrumentTutorial)
            .where(
                SysInstrumentTutorial.instrument_id == query_object.instrument_id if query_object.instrument_id else True,
                SysInstrumentTutorial.tutorial_title == query_object.tutorial_title if query_object.tutorial_title else True,
                SysInstrumentTutorial.tutorial_category == query_object.tutorial_category if query_object.tutorial_category else True,
                SysInstrumentTutorial.tutorial_file == query_object.tutorial_file if query_object.tutorial_file else True,
                SysInstrumentTutorial.tutorial_url == query_object.tutorial_url if query_object.tutorial_url else True,
            )
            .order_by(SysInstrumentTutorial.tutorial_id)
            .distinct()
        )
        instrument_tutorial_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return instrument_tutorial_list

    @classmethod
    async def add_instrument_tutorial_dao(cls, db: AsyncSession, instrument_tutorial: Instrument_tutorialModel):
        """
        新增仪器教程数据库操作

        :param db: orm对象
        :param instrument_tutorial: 仪器教程对象
        :return:
        """
        db_instrument_tutorial = SysInstrumentTutorial(**instrument_tutorial.model_dump(exclude={}))
        db.add(db_instrument_tutorial)
        await db.flush()

        return db_instrument_tutorial

    @classmethod
    async def edit_instrument_tutorial_dao(cls, db: AsyncSession, instrument_tutorial: dict):
        """
        编辑仪器教程数据库操作

        :param db: orm对象
        :param instrument_tutorial: 需要更新的仪器教程字典
        :return:
        """
        await db.execute(update(SysInstrumentTutorial), [instrument_tutorial])

    @classmethod
    async def delete_instrument_tutorial_dao(cls, db: AsyncSession, instrument_tutorial: Instrument_tutorialModel):
        """
        删除仪器教程数据库操作

        :param db: orm对象
        :param instrument_tutorial: 仪器教程对象
        :return:
        """
        await db.execute(delete(SysInstrumentTutorial).where(SysInstrumentTutorial.tutorial_id.in_([instrument_tutorial.tutorial_id])))

