from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.dataset_tag_dao import Dataset_tagDao
from module_admin.entity.vo.dataset_tag_vo import DeleteDataset_tagModel, Dataset_tagModel, Dataset_tagPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Dataset_tagService:
    """
    数据与标签关联模块服务层
    """

    @classmethod
    async def get_dataset_tag_list_services(
        cls, query_db: AsyncSession, query_object: Dataset_tagPageQueryModel, is_page: bool = False
    ):
        """
        获取数据与标签关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据与标签关联列表信息对象
        """
        dataset_tag_list_result = await Dataset_tagDao.get_dataset_tag_list(query_db, query_object, is_page)

        return dataset_tag_list_result


    @classmethod
    async def add_dataset_tag_services(cls, query_db: AsyncSession, page_object: Dataset_tagModel):
        """
        新增数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 新增数据与标签关联对象
        :return: 新增数据与标签关联校验结果
        """
        try:
            await Dataset_tagDao.add_dataset_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_dataset_tag_services(cls, query_db: AsyncSession, page_object: Dataset_tagModel):
        """
        编辑数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 编辑数据与标签关联对象
        :return: 编辑数据与标签关联校验结果
        """
        edit_dataset_tag = page_object.model_dump(exclude_unset=True, exclude={})
        dataset_tag_info = await cls.dataset_tag_detail_services(query_db, page_object.dataset_id)
        if dataset_tag_info.dataset_id:
            try:
                await Dataset_tagDao.edit_dataset_tag_dao(query_db, edit_dataset_tag)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='数据与标签关联不存在')

    @classmethod
    async def delete_dataset_tag_services(cls, query_db: AsyncSession, page_object: DeleteDataset_tagModel):
        """
        删除数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 删除数据与标签关联对象
        :return: 删除数据与标签关联校验结果
        """
        if page_object.dataset_ids:
            dataset_id_list = page_object.dataset_ids.split(',')
            try:
                for dataset_id in dataset_id_list:
                    await Dataset_tagDao.delete_dataset_tag_dao(query_db, Dataset_tagModel(datasetId=dataset_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据ID为空')

    @classmethod
    async def dataset_tag_detail_services(cls, query_db: AsyncSession, dataset_id: int):
        """
        获取数据与标签关联详细信息service

        :param query_db: orm对象
        :param dataset_id: 数据ID
        :return: 数据ID对应的信息
        """
        dataset_tag = await Dataset_tagDao.get_dataset_tag_detail_by_id(query_db, dataset_id=dataset_id)
        if dataset_tag:
            result = Dataset_tagModel(**CamelCaseUtil.transform_result(dataset_tag))
        else:
            result = Dataset_tagModel(**dict())

        return result

    @staticmethod
    async def export_dataset_tag_list_services(dataset_tag_list: List):
        """
        导出数据与标签关联信息service

        :param dataset_tag_list: 数据与标签关联信息列表
        :return: 数据与标签关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'datasetId': '数据ID',
            'tagId': '标签ID',
        }
        binary_data = ExcelUtil.export_list2excel(dataset_tag_list, mapping_dict)

        return binary_data
