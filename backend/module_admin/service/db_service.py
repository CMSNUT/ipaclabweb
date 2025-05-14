from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.db_dao import DbDao
from module_admin.entity.vo.db_vo import DeleteDbModel, DbModel, DbPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class DbService:
    """
    数据集管理模块服务层
    """

    @classmethod
    async def get_db_list_services(
        cls, query_db: AsyncSession, query_object: DbPageQueryModel, is_page: bool = False
    ):
        """
        获取数据集管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据集管理列表信息对象
        """
        db_list_result = await DbDao.get_db_list(query_db, query_object, is_page)

        return db_list_result


    @classmethod
    async def add_db_services(cls, query_db: AsyncSession, page_object: DbModel):
        """
        新增数据集管理信息service

        :param query_db: orm对象
        :param page_object: 新增数据集管理对象
        :return: 新增数据集管理校验结果
        """
        try:
            await DbDao.add_db_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_db_services(cls, query_db: AsyncSession, page_object: DbModel):
        """
        编辑数据集管理信息service

        :param query_db: orm对象
        :param page_object: 编辑数据集管理对象
        :return: 编辑数据集管理校验结果
        """
        edit_db = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        db_info = await cls.db_detail_services(query_db, page_object.db_id)
        if db_info.db_id:
            try:
                await DbDao.edit_db_dao(query_db, edit_db)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='数据集管理不存在')

    @classmethod
    async def delete_db_services(cls, query_db: AsyncSession, page_object: DeleteDbModel):
        """
        删除数据集管理信息service

        :param query_db: orm对象
        :param page_object: 删除数据集管理对象
        :return: 删除数据集管理校验结果
        """
        if page_object.db_ids:
            db_id_list = page_object.db_ids.split(',')
            try:
                for db_id in db_id_list:
                    await DbDao.delete_db_dao(query_db, DbModel(dbId=db_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据id为空')

    @classmethod
    async def db_detail_services(cls, query_db: AsyncSession, db_id: int):
        """
        获取数据集管理详细信息service

        :param query_db: orm对象
        :param db_id: 数据id
        :return: 数据id对应的信息
        """
        db = await DbDao.get_db_detail_by_id(query_db, db_id=db_id)
        if db:
            result = DbModel(**CamelCaseUtil.transform_result(db))
        else:
            result = DbModel(**dict())

        return result

    @staticmethod
    async def export_db_list_services(db_list: List):
        """
        导出数据集管理信息service

        :param db_list: 数据集管理信息列表
        :return: 数据集管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'dbId': '数据id',
            'dbName': '数据名称',
            'dbDesc': '数据简介',
            'dbContent': '数据详情',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(db_list, mapping_dict)

        return binary_data
