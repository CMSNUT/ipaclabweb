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
from module_admin.service.ref_reprod_service import Ref_reprodService
from module_admin.entity.vo.ref_reprod_vo import DeleteRef_reprodModel, Ref_reprodModel, Ref_reprodPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


ref_reprodController = APIRouter(prefix='/system/ref_reprod', dependencies=[Depends(LoginService.get_current_user)])


@ref_reprodController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref_reprod:list'))]
)
async def get_system_ref_reprod_list(
    request: Request,
ref_reprod_page_query: Ref_reprodPageQueryModel = Depends(Ref_reprodPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    ref_reprod_page_query_result = await Ref_reprodService.get_ref_reprod_list_services(query_db, ref_reprod_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=ref_reprod_page_query_result)


@ref_reprodController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_reprod:add'))])
@ValidateFields(validate_model='add_ref_reprod')
@Log(title='文献复现', business_type=BusinessType.INSERT)
async def add_system_ref_reprod(
    request: Request,
    add_ref_reprod: Ref_reprodModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_ref_reprod.create_by = current_user.user.user_name
    add_ref_reprod.create_time = datetime.now()
    add_ref_reprod.update_by = current_user.user.user_name
    add_ref_reprod.update_time = datetime.now()
    add_ref_reprod_result = await Ref_reprodService.add_ref_reprod_services(query_db, add_ref_reprod)
    logger.info(add_ref_reprod_result.message)

    return ResponseUtil.success(msg=add_ref_reprod_result.message)


@ref_reprodController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_reprod:edit'))])
@ValidateFields(validate_model='edit_ref_reprod')
@Log(title='文献复现', business_type=BusinessType.UPDATE)
async def edit_system_ref_reprod(
    request: Request,
    edit_ref_reprod: Ref_reprodModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_ref_reprod.update_by = current_user.user.user_name
    edit_ref_reprod.update_time = datetime.now()
    edit_ref_reprod_result = await Ref_reprodService.edit_ref_reprod_services(query_db, edit_ref_reprod)
    logger.info(edit_ref_reprod_result.message)

    return ResponseUtil.success(msg=edit_ref_reprod_result.message)


@ref_reprodController.delete('/{reprod_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_reprod:remove'))])
@Log(title='文献复现', business_type=BusinessType.DELETE)
async def delete_system_ref_reprod(request: Request, reprod_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_ref_reprod = DeleteRef_reprodModel(reprodIds=reprod_ids)
    delete_ref_reprod_result = await Ref_reprodService.delete_ref_reprod_services(query_db, delete_ref_reprod)
    logger.info(delete_ref_reprod_result.message)

    return ResponseUtil.success(msg=delete_ref_reprod_result.message)


@ref_reprodController.get(
    '/{reprod_id}', response_model=Ref_reprodModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref_reprod:query'))]
)
async def query_detail_system_ref_reprod(request: Request, reprod_id: int, query_db: AsyncSession = Depends(get_db)):
    ref_reprod_detail_result = await Ref_reprodService.ref_reprod_detail_services(query_db, reprod_id)
    logger.info(f'获取reprod_id为{reprod_id}的信息成功')

    return ResponseUtil.success(data=ref_reprod_detail_result)


@ref_reprodController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_reprod:export'))])
@Log(title='文献复现', business_type=BusinessType.EXPORT)
async def export_system_ref_reprod_list(
    request: Request,
    ref_reprod_page_query: Ref_reprodPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    ref_reprod_query_result = await Ref_reprodService.get_ref_reprod_list_services(query_db, ref_reprod_page_query, is_page=False)
    ref_reprod_export_result = await Ref_reprodService.export_ref_reprod_list_services(ref_reprod_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(ref_reprod_export_result))
