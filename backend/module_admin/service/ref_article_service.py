from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.ref_article_dao import Ref_articleDao
from module_admin.entity.vo.ref_article_vo import DeleteRef_articleModel, Ref_articleModel, Ref_articlePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Ref_articleService:
    """
    文献分析模块服务层
    """

    @classmethod
    async def get_ref_article_list_services(
        cls, query_db: AsyncSession, query_object: Ref_articlePageQueryModel, is_page: bool = False
    ):
        """
        获取文献分析列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文献分析列表信息对象
        """
        ref_article_list_result = await Ref_articleDao.get_ref_article_list(query_db, query_object, is_page)

        return ref_article_list_result


    @classmethod
    async def add_ref_article_services(cls, query_db: AsyncSession, page_object: Ref_articleModel):
        """
        新增文献分析信息service

        :param query_db: orm对象
        :param page_object: 新增文献分析对象
        :return: 新增文献分析校验结果
        """
        try:
            await Ref_articleDao.add_ref_article_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_ref_article_services(cls, query_db: AsyncSession, page_object: Ref_articleModel):
        """
        编辑文献分析信息service

        :param query_db: orm对象
        :param page_object: 编辑文献分析对象
        :return: 编辑文献分析校验结果
        """
        edit_ref_article = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        ref_article_info = await cls.ref_article_detail_services(query_db, page_object.article_id)
        if ref_article_info.article_id:
            try:
                await Ref_articleDao.edit_ref_article_dao(query_db, edit_ref_article)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='文献分析不存在')

    @classmethod
    async def delete_ref_article_services(cls, query_db: AsyncSession, page_object: DeleteRef_articleModel):
        """
        删除文献分析信息service

        :param query_db: orm对象
        :param page_object: 删除文献分析对象
        :return: 删除文献分析校验结果
        """
        if page_object.article_ids:
            article_id_list = page_object.article_ids.split(',')
            try:
                for article_id in article_id_list:
                    await Ref_articleDao.delete_ref_article_dao(query_db, Ref_articleModel(articleId=article_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入文章id为空')

    @classmethod
    async def ref_article_detail_services(cls, query_db: AsyncSession, article_id: int):
        """
        获取文献分析详细信息service

        :param query_db: orm对象
        :param article_id: 文章id
        :return: 文章id对应的信息
        """
        ref_article = await Ref_articleDao.get_ref_article_detail_by_id(query_db, article_id=article_id)
        if ref_article:
            result = Ref_articleModel(**CamelCaseUtil.transform_result(ref_article))
        else:
            result = Ref_articleModel(**dict())

        return result

    @staticmethod
    async def export_ref_article_list_services(ref_article_list: List):
        """
        导出文献分析信息service

        :param ref_article_list: 文献分析信息列表
        :return: 文献分析信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'articleId': '文章id',
            'articleName': '文章名称',
            'refId': '文献id',
            'articleContent': '文章内容',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(ref_article_list, mapping_dict)

        return binary_data
