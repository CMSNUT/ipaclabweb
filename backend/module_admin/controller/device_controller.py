from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.device_service import DeviceService
from module_admin.entity.vo.device_vo import DeleteDeviceModel, DeviceModel, DevicePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


deviceController = APIRouter(prefix='/system/device', dependencies=[Depends(LoginService.get_current_user)])


@deviceController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:device:list'))]
)
async def get_system_device_list(
    request: Request,
device_page_query: DevicePageQueryModel = Depends(DevicePageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    device_page_query_result = await DeviceService.get_device_list_services(query_db, device_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=device_page_query_result)


@deviceController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:device:add'))])
@ValidateFields(validate_model='add_device')
@Log(title='仪器信息', business_type=BusinessType.INSERT)
async def add_system_device(
    request: Request,
    add_device: DeviceModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_device.create_by = current_user.user.user_name
    add_device.create_time = datetime.now()
    add_device.update_by = current_user.user.user_name
    add_device.update_time = datetime.now()
    add_device_result = await DeviceService.add_device_services(query_db, add_device)
    logger.info(add_device_result.message)

    return ResponseUtil.success(msg=add_device_result.message)


@deviceController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:device:edit'))])
@ValidateFields(validate_model='edit_device')
@Log(title='仪器信息', business_type=BusinessType.UPDATE)
async def edit_system_device(
    request: Request,
    edit_device: DeviceModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_device.update_by = current_user.user.user_name
    edit_device.update_time = datetime.now()
    edit_device_result = await DeviceService.edit_device_services(query_db, edit_device)
    logger.info(edit_device_result.message)

    return ResponseUtil.success(msg=edit_device_result.message)


@deviceController.delete('/{device_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:device:remove'))])
@Log(title='仪器信息', business_type=BusinessType.DELETE)
async def delete_system_device(request: Request, device_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_device = DeleteDeviceModel(deviceIds=device_ids)
    delete_device_result = await DeviceService.delete_device_services(query_db, delete_device)
    logger.info(delete_device_result.message)

    return ResponseUtil.success(msg=delete_device_result.message)


@deviceController.get(
    '/{device_id}', response_model=DeviceModel, dependencies=[Depends(CheckUserInterfaceAuth('system:device:query'))]
)
async def query_detail_system_device(request: Request, device_id: int, query_db: AsyncSession = Depends(get_db)):
    device_detail_result = await DeviceService.device_detail_services(query_db, device_id)
    logger.info(f'获取device_id为{device_id}的信息成功')

    return ResponseUtil.success(data=device_detail_result)


@deviceController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:device:export'))])
@Log(title='仪器信息', business_type=BusinessType.EXPORT)
async def export_system_device_list(
    request: Request,
    device_page_query: DevicePageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    device_query_result = await DeviceService.get_device_list_services(query_db, device_page_query, is_page=False)
    device_export_result = await DeviceService.export_device_list_services(device_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(device_export_result))
