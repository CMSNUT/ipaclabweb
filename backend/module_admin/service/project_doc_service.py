from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.project_doc_dao import Project_docDao
from module_admin.entity.vo.project_doc_vo import DeleteProject_docModel, Project_docModel, Project_docPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Project_docService:
    """
    项目文档模块服务层
    """

    @classmethod
    async def get_project_doc_list_services(
        cls, query_db: AsyncSession, query_object: Project_docPageQueryModel, is_page: bool = False
    ):
        """
        获取项目文档列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目文档列表信息对象
        """
        project_doc_list_result = await Project_docDao.get_project_doc_list(query_db, query_object, is_page)

        return project_doc_list_result


    @classmethod
    async def add_project_doc_services(cls, query_db: AsyncSession, page_object: Project_docModel):
        """
        新增项目文档信息service

        :param query_db: orm对象
        :param page_object: 新增项目文档对象
        :return: 新增项目文档校验结果
        """
        try:
            await Project_docDao.add_project_doc_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_project_doc_services(cls, query_db: AsyncSession, page_object: Project_docModel):
        """
        编辑项目文档信息service

        :param query_db: orm对象
        :param page_object: 编辑项目文档对象
        :return: 编辑项目文档校验结果
        """
        edit_project_doc = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        project_doc_info = await cls.project_doc_detail_services(query_db, page_object.doc_id)
        if project_doc_info.doc_id:
            try:
                await Project_docDao.edit_project_doc_dao(query_db, edit_project_doc)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='项目文档不存在')

    @classmethod
    async def delete_project_doc_services(cls, query_db: AsyncSession, page_object: DeleteProject_docModel):
        """
        删除项目文档信息service

        :param query_db: orm对象
        :param page_object: 删除项目文档对象
        :return: 删除项目文档校验结果
        """
        if page_object.doc_ids:
            doc_id_list = page_object.doc_ids.split(',')
            try:
                for doc_id in doc_id_list:
                    await Project_docDao.delete_project_doc_dao(query_db, Project_docModel(docId=doc_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入文档id为空')

    @classmethod
    async def project_doc_detail_services(cls, query_db: AsyncSession, doc_id: int):
        """
        获取项目文档详细信息service

        :param query_db: orm对象
        :param doc_id: 文档id
        :return: 文档id对应的信息
        """
        project_doc = await Project_docDao.get_project_doc_detail_by_id(query_db, doc_id=doc_id)
        if project_doc:
            result = Project_docModel(**CamelCaseUtil.transform_result(project_doc))
        else:
            result = Project_docModel(**dict())

        return result

    @staticmethod
    async def export_project_doc_list_services(project_doc_list: List):
        """
        导出项目文档信息service

        :param project_doc_list: 项目文档信息列表
        :return: 项目文档信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'docId': '文档id',
            'docName': '文档名称',
            'projectId': '文献id',
            'docDesc': '文档简介',
            'docContent': '文档内容',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(project_doc_list, mapping_dict)

        return binary_data
