from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.ref_dao import RefDao
from module_admin.entity.vo.ref_vo import DeleteRefModel, RefModel, RefPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class RefService:
    """
    文献管理模块服务层
    """

    @classmethod
    async def get_ref_list_services(
        cls, query_db: AsyncSession, query_object: RefPageQueryModel, is_page: bool = False
    ):
        """
        获取文献管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献管理列表信息对象
        """
        ref_list_result = await RefDao.get_ref_list(query_db, query_object, is_page)

        return ref_list_result


    @classmethod
    async def add_ref_services(cls, query_db: AsyncSession, page_object: RefModel):
        """
        新增文献管理信息service

        :param query_db: orm对象
        :param page_object: 新增文献管理对象
        :return: 新增文献管理校验结果
        """
        try:
            await RefDao.add_ref_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_ref_services(cls, query_db: AsyncSession, page_object: RefModel):
        """
        编辑文献管理信息service

        :param query_db: orm对象
        :param page_object: 编辑文献管理对象
        :return: 编辑文献管理校验结果
        """
        edit_ref = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        ref_info = await cls.ref_detail_services(query_db, page_object.ref_id)
        if ref_info.ref_id:
            try:
                await RefDao.edit_ref_dao(query_db, edit_ref)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='文献管理不存在')

    @classmethod
    async def delete_ref_services(cls, query_db: AsyncSession, page_object: DeleteRefModel):
        """
        删除文献管理信息service

        :param query_db: orm对象
        :param page_object: 删除文献管理对象
        :return: 删除文献管理校验结果
        """
        if page_object.ref_ids:
            ref_id_list = page_object.ref_ids.split(',')
            try:
                for ref_id in ref_id_list:
                    await RefDao.delete_ref_dao(query_db, RefModel(refId=ref_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入文献id为空')

    @classmethod
    async def ref_detail_services(cls, query_db: AsyncSession, ref_id: int):
        """
        获取文献管理详细信息service

        :param query_db: orm对象
        :param ref_id: 文献id
        :return: 文献id对应的信息
        """
        ref = await RefDao.get_ref_detail_by_id(query_db, ref_id=ref_id)
        if ref:
            result = RefModel(**CamelCaseUtil.transform_result(ref))
        else:
            result = RefModel(**dict())

        return result

    @staticmethod
    async def export_ref_list_services(ref_list: List):
        """
        导出文献管理信息service

        :param ref_list: 文献管理信息列表
        :return: 文献管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'refId': '文献id',
            'refTitle': '文献英文标题',
            'refTitleZh': '文献中文标题',
            'refDoi': '文献DOI',
            'refAbs': '文献摘要',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(ref_list, mapping_dict)

        return binary_data
