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
from module_admin.service.instrument_tutorial_service import Instrument_tutorialService
from module_admin.entity.vo.instrument_tutorial_vo import DeleteInstrument_tutorialModel, Instrument_tutorialModel, Instrument_tutorialPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


instrument_tutorialController = APIRouter(prefix='/system/instrument_tutorial', dependencies=[Depends(LoginService.get_current_user)])


@instrument_tutorialController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:instrument_tutorial:list'))]
)
async def get_system_instrument_tutorial_list(
    request: Request,
instrument_tutorial_page_query: Instrument_tutorialPageQueryModel = Depends(Instrument_tutorialPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    instrument_tutorial_page_query_result = await Instrument_tutorialService.get_instrument_tutorial_list_services(query_db, instrument_tutorial_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=instrument_tutorial_page_query_result)


@instrument_tutorialController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument_tutorial:add'))])
@ValidateFields(validate_model='add_instrument_tutorial')
@Log(title='仪器教程', business_type=BusinessType.INSERT)
async def add_system_instrument_tutorial(
    request: Request,
    add_instrument_tutorial: Instrument_tutorialModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_instrument_tutorial.create_by = current_user.user.user_name
    add_instrument_tutorial.create_time = datetime.now()
    add_instrument_tutorial.update_by = current_user.user.user_name
    add_instrument_tutorial.update_time = datetime.now()
    add_instrument_tutorial_result = await Instrument_tutorialService.add_instrument_tutorial_services(query_db, add_instrument_tutorial)
    logger.info(add_instrument_tutorial_result.message)

    return ResponseUtil.success(msg=add_instrument_tutorial_result.message)


@instrument_tutorialController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument_tutorial:edit'))])
@ValidateFields(validate_model='edit_instrument_tutorial')
@Log(title='仪器教程', business_type=BusinessType.UPDATE)
async def edit_system_instrument_tutorial(
    request: Request,
    edit_instrument_tutorial: Instrument_tutorialModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_instrument_tutorial.update_by = current_user.user.user_name
    edit_instrument_tutorial.update_time = datetime.now()
    edit_instrument_tutorial_result = await Instrument_tutorialService.edit_instrument_tutorial_services(query_db, edit_instrument_tutorial)
    logger.info(edit_instrument_tutorial_result.message)

    return ResponseUtil.success(msg=edit_instrument_tutorial_result.message)


@instrument_tutorialController.delete('/{tutorial_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument_tutorial:remove'))])
@Log(title='仪器教程', business_type=BusinessType.DELETE)
async def delete_system_instrument_tutorial(request: Request, tutorial_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_instrument_tutorial = DeleteInstrument_tutorialModel(tutorialIds=tutorial_ids)
    delete_instrument_tutorial_result = await Instrument_tutorialService.delete_instrument_tutorial_services(query_db, delete_instrument_tutorial)
    logger.info(delete_instrument_tutorial_result.message)

    return ResponseUtil.success(msg=delete_instrument_tutorial_result.message)


@instrument_tutorialController.get(
    '/{tutorial_id}', response_model=Instrument_tutorialModel, dependencies=[Depends(CheckUserInterfaceAuth('system:instrument_tutorial:query'))]
)
async def query_detail_system_instrument_tutorial(request: Request, tutorial_id: int, query_db: AsyncSession = Depends(get_db)):
    instrument_tutorial_detail_result = await Instrument_tutorialService.instrument_tutorial_detail_services(query_db, tutorial_id)
    logger.info(f'获取tutorial_id为{tutorial_id}的信息成功')

    return ResponseUtil.success(data=instrument_tutorial_detail_result)


@instrument_tutorialController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument_tutorial:export'))])
@Log(title='仪器教程', business_type=BusinessType.EXPORT)
async def export_system_instrument_tutorial_list(
    request: Request,
    instrument_tutorial_page_query: Instrument_tutorialPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    instrument_tutorial_query_result = await Instrument_tutorialService.get_instrument_tutorial_list_services(query_db, instrument_tutorial_page_query, is_page=False)
    instrument_tutorial_export_result = await Instrument_tutorialService.export_instrument_tutorial_list_services(request, instrument_tutorial_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(instrument_tutorial_export_result))
