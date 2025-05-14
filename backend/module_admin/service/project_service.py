from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.project_dao import ProjectDao
from module_admin.entity.vo.project_vo import DeleteProjectModel, ProjectModel, ProjectPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ProjectService:
    """
    项目管理模块服务层
    """

    @classmethod
    async def get_project_list_services(
        cls, query_db: AsyncSession, query_object: ProjectPageQueryModel, is_page: bool = False
    ):
        """
        获取项目管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目管理列表信息对象
        """
        project_list_result = await ProjectDao.get_project_list(query_db, query_object, is_page)

        return project_list_result


    @classmethod
    async def add_project_services(cls, query_db: AsyncSession, page_object: ProjectModel):
        """
        新增项目管理信息service

        :param query_db: orm对象
        :param page_object: 新增项目管理对象
        :return: 新增项目管理校验结果
        """
        try:
            await ProjectDao.add_project_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_project_services(cls, query_db: AsyncSession, page_object: ProjectModel):
        """
        编辑项目管理信息service

        :param query_db: orm对象
        :param page_object: 编辑项目管理对象
        :return: 编辑项目管理校验结果
        """
        edit_project = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        project_info = await cls.project_detail_services(query_db, page_object.project_id)
        if project_info.project_id:
            try:
                await ProjectDao.edit_project_dao(query_db, edit_project)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='项目管理不存在')

    @classmethod
    async def delete_project_services(cls, query_db: AsyncSession, page_object: DeleteProjectModel):
        """
        删除项目管理信息service

        :param query_db: orm对象
        :param page_object: 删除项目管理对象
        :return: 删除项目管理校验结果
        """
        if page_object.project_ids:
            project_id_list = page_object.project_ids.split(',')
            try:
                for project_id in project_id_list:
                    await ProjectDao.delete_project_dao(query_db, ProjectModel(projectId=project_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入项目id为空')

    @classmethod
    async def project_detail_services(cls, query_db: AsyncSession, project_id: int):
        """
        获取项目管理详细信息service

        :param query_db: orm对象
        :param project_id: 项目id
        :return: 项目id对应的信息
        """
        project = await ProjectDao.get_project_detail_by_id(query_db, project_id=project_id)
        if project:
            result = ProjectModel(**CamelCaseUtil.transform_result(project))
        else:
            result = ProjectModel(**dict())

        return result

    @staticmethod
    async def export_project_list_services(project_list: List):
        """
        导出项目管理信息service

        :param project_list: 项目管理信息列表
        :return: 项目管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'projectId': '项目id',
            'projectTitle': '项目标题',
            'userId': '项目负责人',
            'projectDesc': '项目描述',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(project_list, mapping_dict)

        return binary_data
