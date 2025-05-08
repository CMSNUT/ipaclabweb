from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.service.dict_service import DictDataService
from module_admin.dao.instrument_tutorial_dao import Instrument_tutorialDao
from module_admin.entity.vo.instrument_tutorial_vo import DeleteInstrument_tutorialModel, Instrument_tutorialModel, Instrument_tutorialPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Instrument_tutorialService:
    """
    仪器教程模块服务层
    """

    @classmethod
    async def get_instrument_tutorial_list_services(
        cls, query_db: AsyncSession, query_object: Instrument_tutorialPageQueryModel, is_page: bool = False
    ):
        """
        获取仪器教程列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器教程列表信息对象
        """
        instrument_tutorial_list_result = await Instrument_tutorialDao.get_instrument_tutorial_list(query_db, query_object, is_page)

        return instrument_tutorial_list_result


    @classmethod
    async def add_instrument_tutorial_services(cls, query_db: AsyncSession, page_object: Instrument_tutorialModel):
        """
        新增仪器教程信息service

        :param query_db: orm对象
        :param page_object: 新增仪器教程对象
        :return: 新增仪器教程校验结果
        """
        try:
            await Instrument_tutorialDao.add_instrument_tutorial_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_instrument_tutorial_services(cls, query_db: AsyncSession, page_object: Instrument_tutorialModel):
        """
        编辑仪器教程信息service

        :param query_db: orm对象
        :param page_object: 编辑仪器教程对象
        :return: 编辑仪器教程校验结果
        """
        edit_instrument_tutorial = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        instrument_tutorial_info = await cls.instrument_tutorial_detail_services(query_db, page_object.tutorial_id)
        if instrument_tutorial_info.tutorial_id:
            try:
                await Instrument_tutorialDao.edit_instrument_tutorial_dao(query_db, edit_instrument_tutorial)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='仪器教程不存在')

    @classmethod
    async def delete_instrument_tutorial_services(cls, query_db: AsyncSession, page_object: DeleteInstrument_tutorialModel):
        """
        删除仪器教程信息service

        :param query_db: orm对象
        :param page_object: 删除仪器教程对象
        :return: 删除仪器教程校验结果
        """
        if page_object.tutorial_ids:
            tutorial_id_list = page_object.tutorial_ids.split(',')
            try:
                for tutorial_id in tutorial_id_list:
                    await Instrument_tutorialDao.delete_instrument_tutorial_dao(query_db, Instrument_tutorialModel(tutorialId=tutorial_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入教程ID为空')

    @classmethod
    async def instrument_tutorial_detail_services(cls, query_db: AsyncSession, tutorial_id: int):
        """
        获取仪器教程详细信息service

        :param query_db: orm对象
        :param tutorial_id: 教程ID
        :return: 教程ID对应的信息
        """
        instrument_tutorial = await Instrument_tutorialDao.get_instrument_tutorial_detail_by_id(query_db, tutorial_id=tutorial_id)
        if instrument_tutorial:
            result = Instrument_tutorialModel(**CamelCaseUtil.transform_result(instrument_tutorial))
        else:
            result = Instrument_tutorialModel(**dict())

        return result

    @staticmethod
    async def export_instrument_tutorial_list_services(request: Request, instrument_tutorial_list: List):
        """
        导出仪器教程信息service

        :param instrument_tutorial_list: 仪器教程信息列表
        :return: 仪器教程信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'tutorialId': '教程ID',
            'instrumentId': '仪器ID',
            'tutorialTitle': '教程标题',
            'tutorialCategory': '教程类别',
            'tutorialFile': '本地文件',
            'tutorialUrl': '外部链接',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        sys_tutorial_category_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='sys_tutorial_category'
        )
        sys_tutorial_category_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in sys_tutorial_category_list]
        sys_tutorial_category_option_dict = {item.get('value'): item for item in sys_tutorial_category_option}
        for item in instrument_tutorial_list:
            if str(item.get('tutorialCategory')) in sys_tutorial_category_option_dict.keys():
                item['tutorialCategory'] = sys_tutorial_category_option_dict.get(str(item.get('tutorialCategory'))).get('label')
        binary_data = ExcelUtil.export_list2excel(instrument_tutorial_list, mapping_dict)

        return binary_data
