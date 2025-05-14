from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.algo_tutorial_dao import Algo_tutorialDao
from module_admin.entity.vo.algo_tutorial_vo import DeleteAlgo_tutorialModel, Algo_tutorialModel, Algo_tutorialPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Algo_tutorialService:
    """
    算法教程模块服务层
    """

    @classmethod
    async def get_algo_tutorial_list_services(
        cls, query_db: AsyncSession, query_object: Algo_tutorialPageQueryModel, is_page: bool = False
    ):
        """
        获取算法教程列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 算法教程列表信息对象
        """
        algo_tutorial_list_result = await Algo_tutorialDao.get_algo_tutorial_list(query_db, query_object, is_page)

        return algo_tutorial_list_result


    @classmethod
    async def add_algo_tutorial_services(cls, query_db: AsyncSession, page_object: Algo_tutorialModel):
        """
        新增算法教程信息service

        :param query_db: orm对象
        :param page_object: 新增算法教程对象
        :return: 新增算法教程校验结果
        """
        try:
            await Algo_tutorialDao.add_algo_tutorial_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_algo_tutorial_services(cls, query_db: AsyncSession, page_object: Algo_tutorialModel):
        """
        编辑算法教程信息service

        :param query_db: orm对象
        :param page_object: 编辑算法教程对象
        :return: 编辑算法教程校验结果
        """
        edit_algo_tutorial = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        algo_tutorial_info = await cls.algo_tutorial_detail_services(query_db, page_object.tutorial_id)
        if algo_tutorial_info.tutorial_id:
            try:
                await Algo_tutorialDao.edit_algo_tutorial_dao(query_db, edit_algo_tutorial)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='算法教程不存在')

    @classmethod
    async def delete_algo_tutorial_services(cls, query_db: AsyncSession, page_object: DeleteAlgo_tutorialModel):
        """
        删除算法教程信息service

        :param query_db: orm对象
        :param page_object: 删除算法教程对象
        :return: 删除算法教程校验结果
        """
        if page_object.tutorial_ids:
            tutorial_id_list = page_object.tutorial_ids.split(',')
            try:
                for tutorial_id in tutorial_id_list:
                    await Algo_tutorialDao.delete_algo_tutorial_dao(query_db, Algo_tutorialModel(tutorialId=tutorial_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入教程id为空')

    @classmethod
    async def algo_tutorial_detail_services(cls, query_db: AsyncSession, tutorial_id: int):
        """
        获取算法教程详细信息service

        :param query_db: orm对象
        :param tutorial_id: 教程id
        :return: 教程id对应的信息
        """
        algo_tutorial = await Algo_tutorialDao.get_algo_tutorial_detail_by_id(query_db, tutorial_id=tutorial_id)
        if algo_tutorial:
            result = Algo_tutorialModel(**CamelCaseUtil.transform_result(algo_tutorial))
        else:
            result = Algo_tutorialModel(**dict())

        return result

    @staticmethod
    async def export_algo_tutorial_list_services(algo_tutorial_list: List):
        """
        导出算法教程信息service

        :param algo_tutorial_list: 算法教程信息列表
        :return: 算法教程信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'tutorialId': '教程id',
            'tutorialName': '教程名称',
            'algoId': '算法id',
            'tutorialContent': '教程内容',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(algo_tutorial_list, mapping_dict)

        return binary_data
