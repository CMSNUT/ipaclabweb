from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.instrument_do import SysInstrument
from module_admin.entity.vo.instrument_vo import InstrumentModel, InstrumentPageQueryModel
from utils.page_util import PageUtil


class InstrumentDao:
    """
    仪器信息模块数据库操作层
    """

    @classmethod
    async def get_instrument_detail_by_id(cls, db: AsyncSession, instrument_id: int):
        """
        根据仪器ID获取仪器信息详细信息

        :param db: orm对象
        :param instrument_id: 仪器ID
        :return: 仪器信息信息对象
        """
        instrument_info = (
            (
                await db.execute(
                    select(SysInstrument)
                    .where(
                        SysInstrument.instrument_id == instrument_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return instrument_info

    @classmethod
    async def get_instrument_detail_by_info(cls, db: AsyncSession, instrument: InstrumentModel):
        """
        根据仪器信息参数获取仪器信息信息

        :param db: orm对象
        :param instrument: 仪器信息参数对象
        :return: 仪器信息信息对象
        """
        instrument_info = (
            (
                await db.execute(
                    select(SysInstrument).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return instrument_info

    @classmethod
    async def get_instrument_list(cls, db: AsyncSession, query_object: InstrumentPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取仪器信息列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器信息列表信息对象
        """
        query = (
            select(SysInstrument)
            .where(
                SysInstrument.instrument_name.like(f'%{query_object.instrument_name}%') if query_object.instrument_name else True,
                SysInstrument.instrument_remark.like(f'%{query_object.instrument_remark}%') if query_object.instrument_remark else True,
            )
            .order_by(SysInstrument.instrument_id)
            .distinct()
        )
        instrument_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return instrument_list

    @classmethod
    async def add_instrument_dao(cls, db: AsyncSession, instrument: InstrumentModel):
        """
        新增仪器信息数据库操作

        :param db: orm对象
        :param instrument: 仪器信息对象
        :return:
        """
        db_instrument = SysInstrument(**instrument.model_dump(exclude={}))
        db.add(db_instrument)
        await db.flush()

        return db_instrument

    @classmethod
    async def edit_instrument_dao(cls, db: AsyncSession, instrument: dict):
        """
        编辑仪器信息数据库操作

        :param db: orm对象
        :param instrument: 需要更新的仪器信息字典
        :return:
        """
        await db.execute(update(SysInstrument), [instrument])

    @classmethod
    async def delete_instrument_dao(cls, db: AsyncSession, instrument: InstrumentModel):
        """
        删除仪器信息数据库操作

        :param db: orm对象
        :param instrument: 仪器信息对象
        :return:
        """
        await db.execute(delete(SysInstrument).where(SysInstrument.instrument_id.in_([instrument.instrument_id])))

