from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.project_tag_dao import Project_tagDao
from module_admin.entity.vo.project_tag_vo import DeleteProject_tagModel, Project_tagModel, Project_tagPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Project_tagService:
    """
    数据与标签关联模块服务层
    """

    @classmethod
    async def get_project_tag_list_services(
        cls, query_db: AsyncSession, query_object: Project_tagPageQueryModel, is_page: bool = False
    ):
        """
        获取数据与标签关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据与标签关联列表信息对象
        """
        project_tag_list_result = await Project_tagDao.get_project_tag_list(query_db, query_object, is_page)

        return project_tag_list_result


    @classmethod
    async def add_project_tag_services(cls, query_db: AsyncSession, page_object: Project_tagModel):
        """
        新增数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 新增数据与标签关联对象
        :return: 新增数据与标签关联校验结果
        """
        try:
            await Project_tagDao.add_project_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_project_tag_services(cls, query_db: AsyncSession, page_object: Project_tagModel):
        """
        编辑数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 编辑数据与标签关联对象
        :return: 编辑数据与标签关联校验结果
        """
        edit_project_tag = page_object.model_dump(exclude_unset=True, exclude={})
        project_tag_info = await cls.project_tag_detail_services(query_db, page_object.project_id)
        if project_tag_info.project_id:
            try:
                await Project_tagDao.edit_project_tag_dao(query_db, edit_project_tag)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='数据与标签关联不存在')

    @classmethod
    async def delete_project_tag_services(cls, query_db: AsyncSession, page_object: DeleteProject_tagModel):
        """
        删除数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 删除数据与标签关联对象
        :return: 删除数据与标签关联校验结果
        """
        if page_object.project_ids:
            project_id_list = page_object.project_ids.split(',')
            try:
                for project_id in project_id_list:
                    await Project_tagDao.delete_project_tag_dao(query_db, Project_tagModel(projectId=project_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入项目ID为空')

    @classmethod
    async def project_tag_detail_services(cls, query_db: AsyncSession, project_id: int):
        """
        获取数据与标签关联详细信息service

        :param query_db: orm对象
        :param project_id: 项目ID
        :return: 项目ID对应的信息
        """
        project_tag = await Project_tagDao.get_project_tag_detail_by_id(query_db, project_id=project_id)
        if project_tag:
            result = Project_tagModel(**CamelCaseUtil.transform_result(project_tag))
        else:
            result = Project_tagModel(**dict())

        return result

    @staticmethod
    async def export_project_tag_list_services(project_tag_list: List):
        """
        导出数据与标签关联信息service

        :param project_tag_list: 数据与标签关联信息列表
        :return: 数据与标签关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'projectId': '项目ID',
            'tagId': '标签ID',
        }
        binary_data = ExcelUtil.export_list2excel(project_tag_list, mapping_dict)

        return binary_data
