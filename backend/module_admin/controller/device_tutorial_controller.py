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
from module_admin.service.device_tutorial_service import Device_tutorialService
from module_admin.entity.vo.device_tutorial_vo import DeleteDevice_tutorialModel, Device_tutorialModel, Device_tutorialPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


device_tutorialController = APIRouter(prefix='/system/device_tutorial', dependencies=[Depends(LoginService.get_current_user)])


@device_tutorialController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:device_tutorial:list'))]
)
async def get_system_device_tutorial_list(
    request: Request,
device_tutorial_page_query: Device_tutorialPageQueryModel = Depends(Device_tutorialPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    device_tutorial_page_query_result = await Device_tutorialService.get_device_tutorial_list_services(query_db, device_tutorial_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=device_tutorial_page_query_result)


@device_tutorialController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:device_tutorial:add'))])
@ValidateFields(validate_model='add_device_tutorial')
@Log(title='仪器教程', business_type=BusinessType.INSERT)
async def add_system_device_tutorial(
    request: Request,
    add_device_tutorial: Device_tutorialModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_device_tutorial.create_by = current_user.user.user_name
    add_device_tutorial.create_time = datetime.now()
    add_device_tutorial.update_by = current_user.user.user_name
    add_device_tutorial.update_time = datetime.now()
    add_device_tutorial_result = await Device_tutorialService.add_device_tutorial_services(query_db, add_device_tutorial)
    logger.info(add_device_tutorial_result.message)

    return ResponseUtil.success(msg=add_device_tutorial_result.message)


@device_tutorialController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:device_tutorial:edit'))])
@ValidateFields(validate_model='edit_device_tutorial')
@Log(title='仪器教程', business_type=BusinessType.UPDATE)
async def edit_system_device_tutorial(
    request: Request,
    edit_device_tutorial: Device_tutorialModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_device_tutorial.update_by = current_user.user.user_name
    edit_device_tutorial.update_time = datetime.now()
    edit_device_tutorial_result = await Device_tutorialService.edit_device_tutorial_services(query_db, edit_device_tutorial)
    logger.info(edit_device_tutorial_result.message)

    return ResponseUtil.success(msg=edit_device_tutorial_result.message)


@device_tutorialController.delete('/{tutorial_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:device_tutorial:remove'))])
@Log(title='仪器教程', business_type=BusinessType.DELETE)
async def delete_system_device_tutorial(request: Request, tutorial_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_device_tutorial = DeleteDevice_tutorialModel(tutorialIds=tutorial_ids)
    delete_device_tutorial_result = await Device_tutorialService.delete_device_tutorial_services(query_db, delete_device_tutorial)
    logger.info(delete_device_tutorial_result.message)

    return ResponseUtil.success(msg=delete_device_tutorial_result.message)


@device_tutorialController.get(
    '/{tutorial_id}', response_model=Device_tutorialModel, dependencies=[Depends(CheckUserInterfaceAuth('system:device_tutorial:query'))]
)
async def query_detail_system_device_tutorial(request: Request, tutorial_id: int, query_db: AsyncSession = Depends(get_db)):
    device_tutorial_detail_result = await Device_tutorialService.device_tutorial_detail_services(query_db, tutorial_id)
    logger.info(f'获取tutorial_id为{tutorial_id}的信息成功')

    return ResponseUtil.success(data=device_tutorial_detail_result)


@device_tutorialController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:device_tutorial:export'))])
@Log(title='仪器教程', business_type=BusinessType.EXPORT)
async def export_system_device_tutorial_list(
    request: Request,
    device_tutorial_page_query: Device_tutorialPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    device_tutorial_query_result = await Device_tutorialService.get_device_tutorial_list_services(query_db, device_tutorial_page_query, is_page=False)
    device_tutorial_export_result = await Device_tutorialService.export_device_tutorial_list_services(device_tutorial_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(device_tutorial_export_result))
