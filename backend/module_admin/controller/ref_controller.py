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
from module_admin.service.ref_service import RefService
from module_admin.entity.vo.ref_vo import DeleteRefModel, RefModel, RefPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


refController = APIRouter(prefix='/system/ref', dependencies=[Depends(LoginService.get_current_user)])


@refController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref:list'))]
)
async def get_system_ref_list(
    request: Request,
ref_page_query: RefPageQueryModel = Depends(RefPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    ref_page_query_result = await RefService.get_ref_list_services(query_db, ref_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=ref_page_query_result)


@refController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref:add'))])
@ValidateFields(validate_model='add_ref')
@Log(title='文献管理', business_type=BusinessType.INSERT)
async def add_system_ref(
    request: Request,
    add_ref: RefModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_ref.create_by = current_user.user.user_name
    add_ref.create_time = datetime.now()
    add_ref.update_by = current_user.user.user_name
    add_ref.update_time = datetime.now()
    add_ref_result = await RefService.add_ref_services(query_db, add_ref)
    logger.info(add_ref_result.message)

    return ResponseUtil.success(msg=add_ref_result.message)


@refController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref:edit'))])
@ValidateFields(validate_model='edit_ref')
@Log(title='文献管理', business_type=BusinessType.UPDATE)
async def edit_system_ref(
    request: Request,
    edit_ref: RefModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_ref.update_by = current_user.user.user_name
    edit_ref.update_time = datetime.now()
    edit_ref_result = await RefService.edit_ref_services(query_db, edit_ref)
    logger.info(edit_ref_result.message)

    return ResponseUtil.success(msg=edit_ref_result.message)


@refController.delete('/{ref_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:ref:remove'))])
@Log(title='文献管理', business_type=BusinessType.DELETE)
async def delete_system_ref(request: Request, ref_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_ref = DeleteRefModel(refIds=ref_ids)
    delete_ref_result = await RefService.delete_ref_services(query_db, delete_ref)
    logger.info(delete_ref_result.message)

    return ResponseUtil.success(msg=delete_ref_result.message)


@refController.get(
    '/{ref_id}', response_model=RefModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref:query'))]
)
async def query_detail_system_ref(request: Request, ref_id: int, query_db: AsyncSession = Depends(get_db)):
    ref_detail_result = await RefService.ref_detail_services(query_db, ref_id)
    logger.info(f'获取ref_id为{ref_id}的信息成功')

    return ResponseUtil.success(data=ref_detail_result)


@refController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:ref:export'))])
@Log(title='文献管理', business_type=BusinessType.EXPORT)
async def export_system_ref_list(
    request: Request,
    ref_page_query: RefPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    ref_query_result = await RefService.get_ref_list_services(query_db, ref_page_query, is_page=False)
    ref_export_result = await RefService.export_ref_list_services(ref_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(ref_export_result))
