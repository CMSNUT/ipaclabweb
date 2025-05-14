from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.db_tag_dao import Db_tagDao
from module_admin.entity.vo.db_tag_vo import DeleteDb_tagModel, Db_tagModel, Db_tagPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Db_tagService:
    """
    数据与标签关联模块服务层
    """

    @classmethod
    async def get_db_tag_list_services(
        cls, query_db: AsyncSession, query_object: Db_tagPageQueryModel, is_page: bool = False
    ):
        """
        获取数据与标签关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据与标签关联列表信息对象
        """
        db_tag_list_result = await Db_tagDao.get_db_tag_list(query_db, query_object, is_page)

        return db_tag_list_result


    @classmethod
    async def add_db_tag_services(cls, query_db: AsyncSession, page_object: Db_tagModel):
        """
        新增数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 新增数据与标签关联对象
        :return: 新增数据与标签关联校验结果
        """
        try:
            await Db_tagDao.add_db_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_db_tag_services(cls, query_db: AsyncSession, page_object: Db_tagModel):
        """
        编辑数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 编辑数据与标签关联对象
        :return: 编辑数据与标签关联校验结果
        """
        edit_db_tag = page_object.model_dump(exclude_unset=True, exclude={})
        db_tag_info = await cls.db_tag_detail_services(query_db, page_object.db_id)
        if db_tag_info.db_id:
            try:
                await Db_tagDao.edit_db_tag_dao(query_db, edit_db_tag)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='数据与标签关联不存在')

    @classmethod
    async def delete_db_tag_services(cls, query_db: AsyncSession, page_object: DeleteDb_tagModel):
        """
        删除数据与标签关联信息service

        :param query_db: orm对象
        :param page_object: 删除数据与标签关联对象
        :return: 删除数据与标签关联校验结果
        """
        if page_object.db_ids:
            db_id_list = page_object.db_ids.split(',')
            try:
                for db_id in db_id_list:
                    await Db_tagDao.delete_db_tag_dao(query_db, Db_tagModel(dbId=db_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据ID为空')

    @classmethod
    async def db_tag_detail_services(cls, query_db: AsyncSession, db_id: int):
        """
        获取数据与标签关联详细信息service

        :param query_db: orm对象
        :param db_id: 数据ID
        :return: 数据ID对应的信息
        """
        db_tag = await Db_tagDao.get_db_tag_detail_by_id(query_db, db_id=db_id)
        if db_tag:
            result = Db_tagModel(**CamelCaseUtil.transform_result(db_tag))
        else:
            result = Db_tagModel(**dict())

        return result

    @staticmethod
    async def export_db_tag_list_services(db_tag_list: List):
        """
        导出数据与标签关联信息service

        :param db_tag_list: 数据与标签关联信息列表
        :return: 数据与标签关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'dbId': '数据ID',
            'tagId': '标签ID',
        }
        binary_data = ExcelUtil.export_list2excel(db_tag_list, mapping_dict)

        return binary_data
