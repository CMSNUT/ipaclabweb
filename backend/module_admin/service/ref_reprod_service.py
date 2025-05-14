from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.ref_reprod_dao import Ref_reprodDao
from module_admin.entity.vo.ref_reprod_vo import DeleteRef_reprodModel, Ref_reprodModel, Ref_reprodPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Ref_reprodService:
    """
    文献复现模块服务层
    """

    @classmethod
    async def get_ref_reprod_list_services(
        cls, query_db: AsyncSession, query_object: Ref_reprodPageQueryModel, is_page: bool = False
    ):
        """
        获取文献复现列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献复现列表信息对象
        """
        ref_reprod_list_result = await Ref_reprodDao.get_ref_reprod_list(query_db, query_object, is_page)

        return ref_reprod_list_result


    @classmethod
    async def add_ref_reprod_services(cls, query_db: AsyncSession, page_object: Ref_reprodModel):
        """
        新增文献复现信息service

        :param query_db: orm对象
        :param page_object: 新增文献复现对象
        :return: 新增文献复现校验结果
        """
        try:
            await Ref_reprodDao.add_ref_reprod_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_ref_reprod_services(cls, query_db: AsyncSession, page_object: Ref_reprodModel):
        """
        编辑文献复现信息service

        :param query_db: orm对象
        :param page_object: 编辑文献复现对象
        :return: 编辑文献复现校验结果
        """
        edit_ref_reprod = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        ref_reprod_info = await cls.ref_reprod_detail_services(query_db, page_object.reprod_id)
        if ref_reprod_info.reprod_id:
            try:
                await Ref_reprodDao.edit_ref_reprod_dao(query_db, edit_ref_reprod)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='文献复现不存在')

    @classmethod
    async def delete_ref_reprod_services(cls, query_db: AsyncSession, page_object: DeleteRef_reprodModel):
        """
        删除文献复现信息service

        :param query_db: orm对象
        :param page_object: 删除文献复现对象
        :return: 删除文献复现校验结果
        """
        if page_object.reprod_ids:
            reprod_id_list = page_object.reprod_ids.split(',')
            try:
                for reprod_id in reprod_id_list:
                    await Ref_reprodDao.delete_ref_reprod_dao(query_db, Ref_reprodModel(reprodId=reprod_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入复现id为空')

    @classmethod
    async def ref_reprod_detail_services(cls, query_db: AsyncSession, reprod_id: int):
        """
        获取文献复现详细信息service

        :param query_db: orm对象
        :param reprod_id: 复现id
        :return: 复现id对应的信息
        """
        ref_reprod = await Ref_reprodDao.get_ref_reprod_detail_by_id(query_db, reprod_id=reprod_id)
        if ref_reprod:
            result = Ref_reprodModel(**CamelCaseUtil.transform_result(ref_reprod))
        else:
            result = Ref_reprodModel(**dict())

        return result

    @staticmethod
    async def export_ref_reprod_list_services(ref_reprod_list: List):
        """
        导出文献复现信息service

        :param ref_reprod_list: 文献复现信息列表
        :return: 文献复现信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'reprodId': '复现id',
            'reprodName': '复现名称',
            'refId': '文献id',
            'reprodContent': '复现内容',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(ref_reprod_list, mapping_dict)

        return binary_data
