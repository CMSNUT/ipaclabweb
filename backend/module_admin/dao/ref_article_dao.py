from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.ref_article_do import SysRefArticle
from module_admin.entity.vo.ref_article_vo import Ref_articleModel, Ref_articlePageQueryModel
from utils.page_util import PageUtil


class Ref_articleDao:
    """
    文献分析模块数据库操作层
    """

    @classmethod
    async def get_ref_article_detail_by_id(cls, db: AsyncSession, article_id: int):
        """
        根据文章id获取文献分析详细信息

        :param db: orm对象
        :param article_id: 文章id
        :return: 文献分析信息对象
        """
        ref_article_info = (
            (
                await db.execute(
                    select(SysRefArticle)
                    .where(
                        SysRefArticle.article_id == article_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_article_info

    @classmethod
    async def get_ref_article_detail_by_info(cls, db: AsyncSession, ref_article: Ref_articleModel):
        """
        根据文献分析参数获取文献分析信息

        :param db: orm对象
        :param ref_article: 文献分析参数对象
        :return: 文献分析信息对象
        """
        ref_article_info = (
            (
                await db.execute(
                    select(SysRefArticle).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return ref_article_info

    @classmethod
    async def get_ref_article_list(cls, db: AsyncSession, query_object: Ref_articlePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取文献分析列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献分析列表信息对象
        """
        query = (
            select(SysRefArticle)
            .where(
                SysRefArticle.article_name.like(f'%{query_object.article_name}%') if query_object.article_name else True,
                SysRefArticle.ref_id == query_object.ref_id if query_object.ref_id else True,
                SysRefArticle.article_content.like(f'%{query_object.article_content}%') if query_object.article_content else True,
            )
            .order_by(SysRefArticle.article_id)
            .distinct()
        )
        ref_article_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return ref_article_list

    @classmethod
    async def add_ref_article_dao(cls, db: AsyncSession, ref_article: Ref_articleModel):
        """
        新增文献分析数据库操作

        :param db: orm对象
        :param ref_article: 文献分析对象
        :return:
        """
        db_ref_article = SysRefArticle(**ref_article.model_dump(exclude={}))
        db.add(db_ref_article)
        await db.flush()

        return db_ref_article

    @classmethod
    async def edit_ref_article_dao(cls, db: AsyncSession, ref_article: dict):
        """
        编辑文献分析数据库操作

        :param db: orm对象
        :param ref_article: 需要更新的文献分析字典
        :return:
        """
        await db.execute(update(SysRefArticle), [ref_article])

    @classmethod
    async def delete_ref_article_dao(cls, db: AsyncSession, ref_article: Ref_articleModel):
        """
        删除文献分析数据库操作

        :param db: orm对象
        :param ref_article: 文献分析对象
        :return:
        """
        await db.execute(delete(SysRefArticle).where(SysRefArticle.article_id.in_([ref_article.article_id])))

