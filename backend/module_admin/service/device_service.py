from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.device_dao import DeviceDao
from module_admin.entity.vo.device_vo import DeleteDeviceModel, DeviceModel, DevicePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class DeviceService:
    """
    仪器管理模块服务层
    """

    @classmethod
    async def get_device_list_services(
        cls, query_db: AsyncSession, query_object: DevicePageQueryModel, is_page: bool = False
    ):
        """
        获取仪器管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器管理列表信息对象
        """
        device_list_result = await DeviceDao.get_device_list(query_db, query_object, is_page)

        return device_list_result


    @classmethod
    async def add_device_services(cls, query_db: AsyncSession, page_object: DeviceModel):
        """
        新增仪器管理信息service

        :param query_db: orm对象
        :param page_object: 新增仪器管理对象
        :return: 新增仪器管理校验结果
        """
        try:
            await DeviceDao.add_device_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_device_services(cls, query_db: AsyncSession, page_object: DeviceModel):
        """
        编辑仪器管理信息service

        :param query_db: orm对象
        :param page_object: 编辑仪器管理对象
        :return: 编辑仪器管理校验结果
        """
        edit_device = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        device_info = await cls.device_detail_services(query_db, page_object.device_id)
        if device_info.device_id:
            try:
                await DeviceDao.edit_device_dao(query_db, edit_device)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='仪器管理不存在')

    @classmethod
    async def delete_device_services(cls, query_db: AsyncSession, page_object: DeleteDeviceModel):
        """
        删除仪器管理信息service

        :param query_db: orm对象
        :param page_object: 删除仪器管理对象
        :return: 删除仪器管理校验结果
        """
        if page_object.device_ids:
            device_id_list = page_object.device_ids.split(',')
            try:
                for device_id in device_id_list:
                    await DeviceDao.delete_device_dao(query_db, DeviceModel(deviceId=device_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入仪器id为空')

    @classmethod
    async def device_detail_services(cls, query_db: AsyncSession, device_id: int):
        """
        获取仪器管理详细信息service

        :param query_db: orm对象
        :param device_id: 仪器id
        :return: 仪器id对应的信息
        """
        device = await DeviceDao.get_device_detail_by_id(query_db, device_id=device_id)
        if device:
            result = DeviceModel(**CamelCaseUtil.transform_result(device))
        else:
            result = DeviceModel(**dict())

        return result

    @staticmethod
    async def export_device_list_services(device_list: List):
        """
        导出仪器管理信息service

        :param device_list: 仪器管理信息列表
        :return: 仪器管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'deviceId': '仪器id',
            'deviceName': '仪器名称',
            'deviceImg': '仪器图片地址',
            'deviceDesc': '仪器简介',
            'createBy': '创建人',
            'createTime': '创建时间',
            'updateBy': '更新人',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(device_list, mapping_dict)

        return binary_data
