from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.ref_reprod_do import SysRefReprod
from module_admin.entity.vo.ref_reprod_vo import Ref_reprodModel, Ref_reprodPageQueryModel
from utils.page_util import PageUtil


class Ref_reprodDao:
    """
    文献复现模块数据库操作层
    """

    @classmethod
    async def get_ref_reprod_detail_by_id(cls, db: AsyncSession, reprod_id: int):
        """
        根据复现id获取文献复现详细信息

        :param db: orm对象
        :param reprod_id: 复现id
        :return: 文献复现信息对象
        """
        ref_reprod_info = (
            (
                await db.execute(
                    select(SysRefReprod)
                    .where(
                        SysRefReprod.reprod_id == reprod_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_reprod_info

    @classmethod
    async def get_ref_reprod_detail_by_info(cls, db: AsyncSession, ref_reprod: Ref_reprodModel):
        """
        根据文献复现参数获取文献复现信息

        :param db: orm对象
        :param ref_reprod: 文献复现参数对象
        :return: 文献复现信息对象
        """
        ref_reprod_info = (
            (
                await db.execute(
                    select(SysRefReprod).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_reprod_info

    @classmethod
    async def get_ref_reprod_list(cls, db: AsyncSession, query_object: Ref_reprodPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取文献复现列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献复现列表信息对象
        """
        query = (
            select(SysRefReprod)
            .where(
                SysRefReprod.reprod_name.like(f'%{query_object.reprod_name}%') if query_object.reprod_name else True,
                SysRefReprod.ref_id == query_object.ref_id if query_object.ref_id else True,
                SysRefReprod.reprod_content.like(f'%{query_object.reprod_content}%') if query_object.reprod_content else True,
            )
            .order_by(SysRefReprod.reprod_id)
            .distinct()
        )
        ref_reprod_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return ref_reprod_list

    @classmethod
    async def add_ref_reprod_dao(cls, db: AsyncSession, ref_reprod: Ref_reprodModel):
        """
        新增文献复现数据库操作

        :param db: orm对象
        :param ref_reprod: 文献复现对象
        :return:
        """
        db_ref_reprod = SysRefReprod(**ref_reprod.model_dump(exclude={}))
        db.add(db_ref_reprod)
        await db.flush()

        return db_ref_reprod

    @classmethod
    async def edit_ref_reprod_dao(cls, db: AsyncSession, ref_reprod: dict):
        """
        编辑文献复现数据库操作

        :param db: orm对象
        :param ref_reprod: 需要更新的文献复现字典
        :return:
        """
        await db.execute(update(SysRefReprod), [ref_reprod])

    @classmethod
    async def delete_ref_reprod_dao(cls, db: AsyncSession, ref_reprod: Ref_reprodModel):
        """
        删除文献复现数据库操作

        :param db: orm对象
        :param ref_reprod: 文献复现对象
        :return:
        """
        await db.execute(delete(SysRefReprod).where(SysRefReprod.reprod_id.in_([ref_reprod.reprod_id])))

