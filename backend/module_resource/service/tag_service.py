from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_resource.dao.tag_dao import TagDao
from module_resource.entity.vo.tag_vo import DeleteTagModel, TagModel, TagPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class TagService:
    """
    标签管理模块服务层
    """

    @classmethod
    async def get_tag_list_services(
        cls, query_db: AsyncSession, query_object: TagPageQueryModel, is_page: bool = False
    ):
        """
        获取标签管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标签管理列表信息对象
        """
        tag_list_result = await TagDao.get_tag_list(query_db, query_object, is_page)

        return tag_list_result


    @classmethod
    async def add_tag_services(cls, query_db: AsyncSession, page_object: TagModel):
        """
        新增标签管理信息service

        :param query_db: orm对象
        :param page_object: 新增标签管理对象
        :return: 新增标签管理校验结果
        """
        try:
            await TagDao.add_tag_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_tag_services(cls, query_db: AsyncSession, page_object: TagModel):
        """
        编辑标签管理信息service

        :param query_db: orm对象
        :param page_object: 编辑标签管理对象
        :return: 编辑标签管理校验结果
        """
        edit_tag = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        tag_info = await cls.tag_detail_services(query_db, page_object.tag_id)
        if tag_info.tag_id:
            try:
                await TagDao.edit_tag_dao(query_db, edit_tag)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='标签管理不存在')

    @classmethod
    async def delete_tag_services(cls, query_db: AsyncSession, page_object: DeleteTagModel):
        """
        删除标签管理信息service

        :param query_db: orm对象
        :param page_object: 删除标签管理对象
        :return: 删除标签管理校验结果
        """
        if page_object.tag_ids:
            tag_id_list = page_object.tag_ids.split(',')
            try:
                for tag_id in tag_id_list:
                    await TagDao.delete_tag_dao(query_db, TagModel(tagId=tag_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入标签id为空')

    @classmethod
    async def tag_detail_services(cls, query_db: AsyncSession, tag_id: int):
        """
        获取标签管理详细信息service

        :param query_db: orm对象
        :param tag_id: 标签id
        :return: 标签id对应的信息
        """
        tag = await TagDao.get_tag_detail_by_id(query_db, tag_id=tag_id)
        if tag:
            result = TagModel(**CamelCaseUtil.transform_result(tag))
        else:
            result = TagModel(**dict())

        return result

    @staticmethod
    async def export_tag_list_services(tag_list: List):
        """
        导出标签管理信息service

        :param tag_list: 标签管理信息列表
        :return: 标签管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'tagId': '标签id',
            'tagName': '标签名称',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(tag_list, mapping_dict)

        return binary_data
