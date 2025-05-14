from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.ref_do import SysRef
from module_admin.entity.vo.ref_vo import RefModel, RefPageQueryModel
from utils.page_util import PageUtil


class RefDao:
    """
    文献管理模块数据库操作层
    """

    @classmethod
    async def get_ref_detail_by_id(cls, db: AsyncSession, ref_id: int):
        """
        根据文献id获取文献管理详细信息

        :param db: orm对象
        :param ref_id: 文献id
        :return: 文献管理信息对象
        """
        ref_info = (
            (
                await db.execute(
                    select(SysRef)
                    .where(
                        SysRef.ref_id == ref_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_info

    @classmethod
    async def get_ref_detail_by_info(cls, db: AsyncSession, ref: RefModel):
        """
        根据文献管理参数获取文献管理信息

        :param db: orm对象
        :param ref: 文献管理参数对象
        :return: 文献管理信息对象
        """
        ref_info = (
            (
                await db.execute(
                    select(SysRef).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_info

    @classmethod
    async def get_ref_list(cls, db: AsyncSession, query_object: RefPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取文献管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献管理列表信息对象
        """
        query = (
            select(SysRef)
            .where(
                SysRef.ref_title.like(f'%{query_object.ref_title}%') if query_object.ref_title else True,
                SysRef.ref_title_zh.like(f'%{query_object.ref_title_zh}%') if query_object.ref_title_zh else True,
                SysRef.ref_doi == query_object.ref_doi if query_object.ref_doi else True,
                SysRef.ref_abs.like(f'%{query_object.ref_abs}%') if query_object.ref_abs else True,
            )
            .order_by(SysRef.ref_id)
            .distinct()
        )
        ref_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return ref_list

    @classmethod
    async def add_ref_dao(cls, db: AsyncSession, ref: RefModel):
        """
        新增文献管理数据库操作

        :param db: orm对象
        :param ref: 文献管理对象
        :return:
        """
        db_ref = SysRef(**ref.model_dump(exclude={}))
        db.add(db_ref)
        await db.flush()

        return db_ref

    @classmethod
    async def edit_ref_dao(cls, db: AsyncSession, ref: dict):
        """
        编辑文献管理数据库操作

        :param db: orm对象
        :param ref: 需要更新的文献管理字典
        :return:
        """
        await db.execute(update(SysRef), [ref])

    @classmethod
    async def delete_ref_dao(cls, db: AsyncSession, ref: RefModel):
        """
        删除文献管理数据库操作

        :param db: orm对象
        :param ref: 文献管理对象
        :return:
        """
        await db.execute(delete(SysRef).where(SysRef.ref_id.in_([ref.ref_id])))

