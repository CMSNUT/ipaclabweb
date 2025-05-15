from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_resource.dao.algo_tag_dao import Algo_tagDao
from module_resource.entity.vo.algo_tag_vo import DeleteAlgo_tagModel, Algo_tagModel, Algo_tagPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Algo_tagService:
    """
    算法与标签关联模块服务层
    """

    @classmethod
    async def get_algo_tag_list_services(
        cls, query_db: AsyncSession, query_object: Algo_tagPageQueryModel, is_page: bool = False
    ):
        """
        获取算法与标签关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 算法与标签关联列表信息对象
        """
        algo_tag_list_result = await Algo_tagDao.get_algo_tag_list(query_db, query_object, is_page)

        return algo_tag_list_result


    @classmethod
    async def add_algo_tag_services(cls, query_db: AsyncSession, page_object: Algo_tagModel):
        """
        新增算法与标签关联信息service

        :param query_db: orm对象
        :param page_object: 新增算法与标签关联对象
        :return: 新增算法与标签关联校验结果
        """
        try:
            await Algo_tagDao.add_algo_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_algo_tag_services(cls, query_db: AsyncSession, page_object: Algo_tagModel):
        """
        编辑算法与标签关联信息service

        :param query_db: orm对象
        :param page_object: 编辑算法与标签关联对象
        :return: 编辑算法与标签关联校验结果
        """
        edit_algo_tag = page_object.model_dump(exclude_unset=True, exclude={})
        algo_tag_info = await cls.algo_tag_detail_services(query_db, page_object.algo_id)
        if algo_tag_info.algo_id:
            try:
                await Algo_tagDao.edit_algo_tag_dao(query_db, edit_algo_tag)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='算法与标签关联不存在')

    @classmethod
    async def delete_algo_tag_services(cls, query_db: AsyncSession, page_object: DeleteAlgo_tagModel):
        """
        删除算法与标签关联信息service

        :param query_db: orm对象
        :param page_object: 删除算法与标签关联对象
        :return: 删除算法与标签关联校验结果
        """
        if page_object.algo_ids:
            algo_id_list = page_object.algo_ids.split(',')
            try:
                for algo_id in algo_id_list:
                    await Algo_tagDao.delete_algo_tag_dao(query_db, Algo_tagModel(algoId=algo_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入算法ID为空')

    @classmethod
    async def algo_tag_detail_services(cls, query_db: AsyncSession, algo_id: int):
        """
        获取算法与标签关联详细信息service

        :param query_db: orm对象
        :param algo_id: 算法ID
        :return: 算法ID对应的信息
        """
        algo_tag = await Algo_tagDao.get_algo_tag_detail_by_id(query_db, algo_id=algo_id)
        if algo_tag:
            result = Algo_tagModel(**CamelCaseUtil.transform_result(algo_tag))
        else:
            result = Algo_tagModel(**dict())

        return result

    @staticmethod
    async def export_algo_tag_list_services(algo_tag_list: List):
        """
        导出算法与标签关联信息service

        :param algo_tag_list: 算法与标签关联信息列表
        :return: 算法与标签关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'algoId': '算法ID',
            'tagId': '标签ID',
        }
        binary_data = ExcelUtil.export_list2excel(algo_tag_list, mapping_dict)

        return binary_data
