from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.ref_tag_dao import Ref_tagDao
from module_admin.entity.vo.ref_tag_vo import DeleteRef_tagModel, Ref_tagModel, Ref_tagPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Ref_tagService:
    """
    文献与标签关联模块服务层
    """

    @classmethod
    async def get_ref_tag_list_services(
        cls, query_db: AsyncSession, query_object: Ref_tagPageQueryModel, is_page: bool = False
    ):
        """
        获取文献与标签关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献与标签关联列表信息对象
        """
        ref_tag_list_result = await Ref_tagDao.get_ref_tag_list(query_db, query_object, is_page)

        return ref_tag_list_result


    @classmethod
    async def add_ref_tag_services(cls, query_db: AsyncSession, page_object: Ref_tagModel):
        """
        新增文献与标签关联信息service

        :param query_db: orm对象
        :param page_object: 新增文献与标签关联对象
        :return: 新增文献与标签关联校验结果
        """
        try:
            await Ref_tagDao.add_ref_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_ref_tag_services(cls, query_db: AsyncSession, page_object: Ref_tagModel):
        """
        编辑文献与标签关联信息service

        :param query_db: orm对象
        :param page_object: 编辑文献与标签关联对象
        :return: 编辑文献与标签关联校验结果
        """
        edit_ref_tag = page_object.model_dump(exclude_unset=True, exclude={})
        ref_tag_info = await cls.ref_tag_detail_services(query_db, page_object.ref_id)
        if ref_tag_info.ref_id:
            try:
                await Ref_tagDao.edit_ref_tag_dao(query_db, edit_ref_tag)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='文献与标签关联不存在')

    @classmethod
    async def delete_ref_tag_services(cls, query_db: AsyncSession, page_object: DeleteRef_tagModel):
        """
        删除文献与标签关联信息service

        :param query_db: orm对象
        :param page_object: 删除文献与标签关联对象
        :return: 删除文献与标签关联校验结果
        """
        if page_object.ref_ids:
            ref_id_list = page_object.ref_ids.split(',')
            try:
                for ref_id in ref_id_list:
                    await Ref_tagDao.delete_ref_tag_dao(query_db, Ref_tagModel(refId=ref_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入文献ID为空')

    @classmethod
    async def ref_tag_detail_services(cls, query_db: AsyncSession, ref_id: int):
        """
        获取文献与标签关联详细信息service

        :param query_db: orm对象
        :param ref_id: 文献ID
        :return: 文献ID对应的信息
        """
        ref_tag = await Ref_tagDao.get_ref_tag_detail_by_id(query_db, ref_id=ref_id)
        if ref_tag:
            result = Ref_tagModel(**CamelCaseUtil.transform_result(ref_tag))
        else:
            result = Ref_tagModel(**dict())

        return result

    @staticmethod
    async def export_ref_tag_list_services(ref_tag_list: List):
        """
        导出文献与标签关联信息service

        :param ref_tag_list: 文献与标签关联信息列表
        :return: 文献与标签关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'refId': '文献ID',
            'tagId': '标签ID',
        }
        binary_data = ExcelUtil.export_list2excel(ref_tag_list, mapping_dict)

        return binary_data
