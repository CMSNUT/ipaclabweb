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
from module_admin.service.instrument_service import InstrumentService
from module_admin.entity.vo.instrument_vo import DeleteInstrumentModel, InstrumentModel, InstrumentPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


instrumentController = APIRouter(prefix='/system/instrument', dependencies=[Depends(LoginService.get_current_user)])


@instrumentController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:instrument:list'))]
)
async def get_system_instrument_list(
    request: Request,
instrument_page_query: InstrumentPageQueryModel = Depends(InstrumentPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    instrument_page_query_result = await InstrumentService.get_instrument_list_services(query_db, instrument_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=instrument_page_query_result)


@instrumentController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument:add'))])
@ValidateFields(validate_model='add_instrument')
@Log(title='仪器信息', business_type=BusinessType.INSERT)
async def add_system_instrument(
    request: Request,
    add_instrument: InstrumentModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_instrument.create_by = current_user.user.user_name
    add_instrument.create_time = datetime.now()
    add_instrument.update_by = current_user.user.user_name
    add_instrument.update_time = datetime.now()
    add_instrument_result = await InstrumentService.add_instrument_services(query_db, add_instrument)
    logger.info(add_instrument_result.message)

    return ResponseUtil.success(msg=add_instrument_result.message)


@instrumentController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument:edit'))])
@ValidateFields(validate_model='edit_instrument')
@Log(title='仪器信息', business_type=BusinessType.UPDATE)
async def edit_system_instrument(
    request: Request,
    edit_instrument: InstrumentModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_instrument.update_by = current_user.user.user_name
    edit_instrument.update_time = datetime.now()
    edit_instrument_result = await InstrumentService.edit_instrument_services(query_db, edit_instrument)
    logger.info(edit_instrument_result.message)

    return ResponseUtil.success(msg=edit_instrument_result.message)


@instrumentController.delete('/{instrument_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument:remove'))])
@Log(title='仪器信息', business_type=BusinessType.DELETE)
async def delete_system_instrument(request: Request, instrument_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_instrument = DeleteInstrumentModel(instrumentIds=instrument_ids)
    delete_instrument_result = await InstrumentService.delete_instrument_services(query_db, delete_instrument)
    logger.info(delete_instrument_result.message)

    return ResponseUtil.success(msg=delete_instrument_result.message)


@instrumentController.get(
    '/{instrument_id}', response_model=InstrumentModel, dependencies=[Depends(CheckUserInterfaceAuth('system:instrument:query'))]
)
async def query_detail_system_instrument(request: Request, instrument_id: int, query_db: AsyncSession = Depends(get_db)):
    instrument_detail_result = await InstrumentService.instrument_detail_services(query_db, instrument_id)
    logger.info(f'获取instrument_id为{instrument_id}的信息成功')

    return ResponseUtil.success(data=instrument_detail_result)


@instrumentController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:instrument:export'))])
@Log(title='仪器信息', business_type=BusinessType.EXPORT)
async def export_system_instrument_list(
    request: Request,
    instrument_page_query: InstrumentPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    instrument_query_result = await InstrumentService.get_instrument_list_services(query_db, instrument_page_query, is_page=False)
    instrument_export_result = await InstrumentService.export_instrument_list_services(instrument_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(instrument_export_result))
