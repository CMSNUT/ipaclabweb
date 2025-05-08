from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.instrument_dao import InstrumentDao
from module_admin.entity.vo.instrument_vo import DeleteInstrumentModel, InstrumentModel, InstrumentPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class InstrumentService:
    """
    仪器信息模块服务层
    """

    @classmethod
    async def get_instrument_list_services(
        cls, query_db: AsyncSession, query_object: InstrumentPageQueryModel, is_page: bool = False
    ):
        """
        获取仪器信息列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器信息列表信息对象
        """
        instrument_list_result = await InstrumentDao.get_instrument_list(query_db, query_object, is_page)

        return instrument_list_result


    @classmethod
    async def add_instrument_services(cls, query_db: AsyncSession, page_object: InstrumentModel):
        """
        新增仪器信息信息service

        :param query_db: orm对象
        :param page_object: 新增仪器信息对象
        :return: 新增仪器信息校验结果
        """
        try:
            await InstrumentDao.add_instrument_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_instrument_services(cls, query_db: AsyncSession, page_object: InstrumentModel):
        """
        编辑仪器信息信息service

        :param query_db: orm对象
        :param page_object: 编辑仪器信息对象
        :return: 编辑仪器信息校验结果
        """
        edit_instrument = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        instrument_info = await cls.instrument_detail_services(query_db, page_object.instrument_id)
        if instrument_info.instrument_id:
            try:
                await InstrumentDao.edit_instrument_dao(query_db, edit_instrument)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='仪器信息不存在')

    @classmethod
    async def delete_instrument_services(cls, query_db: AsyncSession, page_object: DeleteInstrumentModel):
        """
        删除仪器信息信息service

        :param query_db: orm对象
        :param page_object: 删除仪器信息对象
        :return: 删除仪器信息校验结果
        """
        if page_object.instrument_ids:
            instrument_id_list = page_object.instrument_ids.split(',')
            try:
                for instrument_id in instrument_id_list:
                    await InstrumentDao.delete_instrument_dao(query_db, InstrumentModel(instrumentId=instrument_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入仪器ID为空')

    @classmethod
    async def instrument_detail_services(cls, query_db: AsyncSession, instrument_id: int):
        """
        获取仪器信息详细信息service

        :param query_db: orm对象
        :param instrument_id: 仪器ID
        :return: 仪器ID对应的信息
        """
        instrument = await InstrumentDao.get_instrument_detail_by_id(query_db, instrument_id=instrument_id)
        if instrument:
            result = InstrumentModel(**CamelCaseUtil.transform_result(instrument))
        else:
            result = InstrumentModel(**dict())

        return result

    @staticmethod
    async def export_instrument_list_services(instrument_list: List):
        """
        导出仪器信息信息service

        :param instrument_list: 仪器信息信息列表
        :return: 仪器信息信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'instrumentId': '仪器ID',
            'instrumentName': '仪器名称',
            'instrumentModel': '仪器型号',
            'instrumentRemark': '功能简介',
            'instrumentRoom': '存放位置',
            'instrumentImg': '图片地址',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(instrument_list, mapping_dict)

        return binary_data
