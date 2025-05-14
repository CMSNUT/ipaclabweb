from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.project_member_dao import Project_memberDao
from module_admin.entity.vo.project_member_vo import DeleteProject_memberModel, Project_memberModel, Project_memberPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Project_memberService:
    """
    项目与用户关联模块服务层
    """

    @classmethod
    async def get_project_member_list_services(
        cls, query_db: AsyncSession, query_object: Project_memberPageQueryModel, is_page: bool = False
    ):
        """
        获取项目与用户关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目与用户关联列表信息对象
        """
        project_member_list_result = await Project_memberDao.get_project_member_list(query_db, query_object, is_page)

        return project_member_list_result


    @classmethod
    async def add_project_member_services(cls, query_db: AsyncSession, page_object: Project_memberModel):
        """
        新增项目与用户关联信息service

        :param query_db: orm对象
        :param page_object: 新增项目与用户关联对象
        :return: 新增项目与用户关联校验结果
        """
        try:
            await Project_memberDao.add_project_member_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_project_member_services(cls, query_db: AsyncSession, page_object: Project_memberModel):
        """
        编辑项目与用户关联信息service

        :param query_db: orm对象
        :param page_object: 编辑项目与用户关联对象
        :return: 编辑项目与用户关联校验结果
        """
        edit_project_member = page_object.model_dump(exclude_unset=True, exclude={})
        project_member_info = await cls.project_member_detail_services(query_db, page_object.project_id)
        if project_member_info.project_id:
            try:
                await Project_memberDao.edit_project_member_dao(query_db, edit_project_member)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='项目与用户关联不存在')

    @classmethod
    async def delete_project_member_services(cls, query_db: AsyncSession, page_object: DeleteProject_memberModel):
        """
        删除项目与用户关联信息service

        :param query_db: orm对象
        :param page_object: 删除项目与用户关联对象
        :return: 删除项目与用户关联校验结果
        """
        if page_object.project_ids:
            project_id_list = page_object.project_ids.split(',')
            try:
                for project_id in project_id_list:
                    await Project_memberDao.delete_project_member_dao(query_db, Project_memberModel(projectId=project_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据ID为空')

    @classmethod
    async def project_member_detail_services(cls, query_db: AsyncSession, project_id: int):
        """
        获取项目与用户关联详细信息service

        :param query_db: orm对象
        :param project_id: 数据ID
        :return: 数据ID对应的信息
        """
        project_member = await Project_memberDao.get_project_member_detail_by_id(query_db, project_id=project_id)
        if project_member:
            result = Project_memberModel(**CamelCaseUtil.transform_result(project_member))
        else:
            result = Project_memberModel(**dict())

        return result

    @staticmethod
    async def export_project_member_list_services(project_member_list: List):
        """
        导出项目与用户关联信息service

        :param project_member_list: 项目与用户关联信息列表
        :return: 项目与用户关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'projectId': '数据ID',
            'userId': '标签ID',
            'memberRole': '项目分工',
        }
        binary_data = ExcelUtil.export_list2excel(project_member_list, mapping_dict)

        return binary_data
