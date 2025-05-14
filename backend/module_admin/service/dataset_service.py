from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.dataset_dao import DatasetDao
from module_admin.entity.vo.dataset_vo import DeleteDatasetModel, DatasetModel, DatasetPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class DatasetService:
    """
    数据管理模块服务层
    """

    @classmethod
    async def get_dataset_list_services(
        cls, query_db: AsyncSession, query_object: DatasetPageQueryModel, is_page: bool = False
    ):
        """
        获取数据管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据管理列表信息对象
        """
        dataset_list_result = await DatasetDao.get_dataset_list(query_db, query_object, is_page)

        return dataset_list_result


    @classmethod
    async def add_dataset_services(cls, query_db: AsyncSession, page_object: DatasetModel):
        """
        新增数据管理信息service

        :param query_db: orm对象
        :param page_object: 新增数据管理对象
        :return: 新增数据管理校验结果
        """
        try:
            await DatasetDao.add_dataset_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_dataset_services(cls, query_db: AsyncSession, page_object: DatasetModel):
        """
        编辑数据管理信息service

        :param query_db: orm对象
        :param page_object: 编辑数据管理对象
        :return: 编辑数据管理校验结果
        """
        edit_dataset = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        dataset_info = await cls.dataset_detail_services(query_db, page_object.dataset_id)
        if dataset_info.dataset_id:
            try:
                await DatasetDao.edit_dataset_dao(query_db, edit_dataset)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='数据管理不存在')

    @classmethod
    async def delete_dataset_services(cls, query_db: AsyncSession, page_object: DeleteDatasetModel):
        """
        删除数据管理信息service

        :param query_db: orm对象
        :param page_object: 删除数据管理对象
        :return: 删除数据管理校验结果
        """
        if page_object.dataset_ids:
            dataset_id_list = page_object.dataset_ids.split(',')
            try:
                for dataset_id in dataset_id_list:
                    await DatasetDao.delete_dataset_dao(query_db, DatasetModel(datasetId=dataset_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据id为空')

    @classmethod
    async def dataset_detail_services(cls, query_db: AsyncSession, dataset_id: int):
        """
        获取数据管理详细信息service

        :param query_db: orm对象
        :param dataset_id: 数据id
        :return: 数据id对应的信息
        """
        dataset = await DatasetDao.get_dataset_detail_by_id(query_db, dataset_id=dataset_id)
        if dataset:
            result = DatasetModel(**CamelCaseUtil.transform_result(dataset))
        else:
            result = DatasetModel(**dict())

        return result

    @staticmethod
    async def export_dataset_list_services(dataset_list: List):
        """
        导出数据管理信息service

        :param dataset_list: 数据管理信息列表
        :return: 数据管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'datasetId': '数据id',
            'datasetName': '数据名称',
            'datasetDesc': '数据简介',
            'datasetContent': '数据详情',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(dataset_list, mapping_dict)

        return binary_data
