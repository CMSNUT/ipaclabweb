from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.project_doc_do import SysProjectDoc
from module_admin.entity.vo.project_doc_vo import Project_docModel, Project_docPageQueryModel
from utils.page_util import PageUtil


class Project_docDao:
    """
    项目文档模块数据库操作层
    """

    @classmethod
    async def get_project_doc_detail_by_id(cls, db: AsyncSession, doc_id: int):
        """
        根据文档id获取项目文档详细信息

        :param db: orm对象
        :param doc_id: 文档id
        :return: 项目文档信息对象
        """
        project_doc_info = (
            (
                await db.execute(
                    select(SysProjectDoc)
                    .where(
                        SysProjectDoc.doc_id == doc_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_doc_info

    @classmethod
    async def get_project_doc_detail_by_info(cls, db: AsyncSession, project_doc: Project_docModel):
        """
        根据项目文档参数获取项目文档信息

        :param db: orm对象
        :param project_doc: 项目文档参数对象
        :return: 项目文档信息对象
        """
        project_doc_info = (
            (
                await db.execute(
                    select(SysProjectDoc).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_doc_info

    @classmethod
    async def get_project_doc_list(cls, db: AsyncSession, query_object: Project_docPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取项目文档列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目文档列表信息对象
        """
        query = (
            select(SysProjectDoc)
            .where(
                SysProjectDoc.doc_name.like(f'%{query_object.doc_name}%') if query_object.doc_name else True,
                SysProjectDoc.project_id == query_object.project_id if query_object.project_id else True,
                SysProjectDoc.doc_desc.like(f'%{query_object.doc_desc}%') if query_object.doc_desc else True,
                SysProjectDoc.doc_content.like(f'%{query_object.doc_content}%') if query_object.doc_content else True,
            )
            .order_by(SysProjectDoc.doc_id)
            .distinct()
        )
        project_doc_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return project_doc_list

    @classmethod
    async def add_project_doc_dao(cls, db: AsyncSession, project_doc: Project_docModel):
        """
        新增项目文档数据库操作

        :param db: orm对象
        :param project_doc: 项目文档对象
        :return:
        """
        db_project_doc = SysProjectDoc(**project_doc.model_dump(exclude={}))
        db.add(db_project_doc)
        await db.flush()

        return db_project_doc

    @classmethod
    async def edit_project_doc_dao(cls, db: AsyncSession, project_doc: dict):
        """
        编辑项目文档数据库操作

        :param db: orm对象
        :param project_doc: 需要更新的项目文档字典
        :return:
        """
        await db.execute(update(SysProjectDoc), [project_doc])

    @classmethod
    async def delete_project_doc_dao(cls, db: AsyncSession, project_doc: Project_docModel):
        """
        删除项目文档数据库操作

        :param db: orm对象
        :param project_doc: 项目文档对象
        :return:
        """
        await db.execute(delete(SysProjectDoc).where(SysProjectDoc.doc_id.in_([project_doc.doc_id])))

