from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.service.dict_service import DictDataService
from module_resource.dao.algo_dao import AlgoDao
from module_resource.entity.vo.algo_vo import DeleteAlgoModel, AlgoModel, AlgoPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class AlgoService:
    """
    算法管理模块服务层
    """

    @classmethod
    async def get_algo_list_services(
        cls, query_db: AsyncSession, query_object: AlgoPageQueryModel, is_page: bool = False
    ):
        """
        获取算法管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 算法管理列表信息对象
        """
        algo_list_result = await AlgoDao.get_algo_list(query_db, query_object, is_page)

        return algo_list_result


    @classmethod
    async def add_algo_services(cls, query_db: AsyncSession, page_object: AlgoModel):
        """
        新增算法管理信息service

        :param query_db: orm对象
        :param page_object: 新增算法管理对象
        :return: 新增算法管理校验结果
        """
        try:
            await AlgoDao.add_algo_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_algo_services(cls, query_db: AsyncSession, page_object: AlgoModel):
        """
        编辑算法管理信息service

        :param query_db: orm对象
        :param page_object: 编辑算法管理对象
        :return: 编辑算法管理校验结果
        """
        edit_algo = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        algo_info = await cls.algo_detail_services(query_db, page_object.algo_id)
        if algo_info.algo_id:
            try:
                await AlgoDao.edit_algo_dao(query_db, edit_algo)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='算法管理不存在')

    @classmethod
    async def delete_algo_services(cls, query_db: AsyncSession, page_object: DeleteAlgoModel):
        """
        删除算法管理信息service

        :param query_db: orm对象
        :param page_object: 删除算法管理对象
        :return: 删除算法管理校验结果
        """
        if page_object.algo_ids:
            algo_id_list = page_object.algo_ids.split(',')
            try:
                for algo_id in algo_id_list:
                    await AlgoDao.delete_algo_dao(query_db, AlgoModel(algoId=algo_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入算法id为空')

    @classmethod
    async def algo_detail_services(cls, query_db: AsyncSession, algo_id: int):
        """
        获取算法管理详细信息service

        :param query_db: orm对象
        :param algo_id: 算法id
        :return: 算法id对应的信息
        """
        algo = await AlgoDao.get_algo_detail_by_id(query_db, algo_id=algo_id)
        if algo:
            result = AlgoModel(**CamelCaseUtil.transform_result(algo))
        else:
            result = AlgoModel(**dict())

        return result

    @staticmethod
    async def export_algo_list_services(request: Request, algo_list: List):
        """
        导出算法管理信息service

        :param algo_list: 算法管理信息列表
        :return: 算法管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'algoId': '算法id',
            'algoName': '算法名称',
            'algoType': '算法类别',
            'algoLang': '算法语言',
            'algoContent': '算法详情',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        sys_algo_lang_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='sys_algo_lang'
        )
        sys_algo_lang_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in sys_algo_lang_list]
        sys_algo_lang_option_dict = {item.get('value'): item for item in sys_algo_lang_option}
        sys_algo_type_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='sys_algo_type'
        )
        sys_algo_type_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in sys_algo_type_list]
        sys_algo_type_option_dict = {item.get('value'): item for item in sys_algo_type_option}
        for item in algo_list:
            if str(item.get('algoType')) in sys_algo_type_option_dict.keys():
                item['algoType'] = sys_algo_type_option_dict.get(str(item.get('algoType'))).get('label')
            if str(item.get('algoLang')) in sys_algo_lang_option_dict.keys():
                item['algoLang'] = sys_algo_lang_option_dict.get(str(item.get('algoLang'))).get('label')
        binary_data = ExcelUtil.export_list2excel(algo_list, mapping_dict)

        return binary_data
