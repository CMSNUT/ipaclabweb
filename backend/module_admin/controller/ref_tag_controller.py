from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.ref_tag_service import Ref_tagService
from module_admin.entity.vo.ref_tag_vo import DeleteRef_tagModel, Ref_tagModel, Ref_tagPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


ref_tagController = APIRouter(prefix='/system/ref_tag', dependencies=[Depends(LoginService.get_current_user)])


@ref_tagController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref_tag:list'))]
)
async def get_system_ref_tag_list(
    request: Request,
ref_tag_page_query: Ref_tagPageQueryModel = Depends(Ref_tagPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    ref_tag_page_query_result = await Ref_tagService.get_ref_tag_list_services(query_db, ref_tag_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=ref_tag_page_query_result)


@ref_tagController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_tag:add'))])
@ValidateFields(validate_model='add_ref_tag')
@Log(title='文献与标签关联', business_type=BusinessType.INSERT)
async def add_system_ref_tag(
    request: Request,
    add_ref_tag: Ref_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_ref_tag_result = await Ref_tagService.add_ref_tag_services(query_db, add_ref_tag)
    logger.info(add_ref_tag_result.message)

    return ResponseUtil.success(msg=add_ref_tag_result.message)


@ref_tagController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_tag:edit'))])
@ValidateFields(validate_model='edit_ref_tag')
@Log(title='文献与标签关联', business_type=BusinessType.UPDATE)
async def edit_system_ref_tag(
    request: Request,
    edit_ref_tag: Ref_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_ref_tag.update_by = current_user.user.user_name
    edit_ref_tag.update_time = datetime.now()
    edit_ref_tag_result = await Ref_tagService.edit_ref_tag_services(query_db, edit_ref_tag)
    logger.info(edit_ref_tag_result.message)

    return ResponseUtil.success(msg=edit_ref_tag_result.message)


@ref_tagController.delete('/{ref_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_tag:remove'))])
@Log(title='文献与标签关联', business_type=BusinessType.DELETE)
async def delete_system_ref_tag(request: Request, ref_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_ref_tag = DeleteRef_tagModel(refIds=ref_ids)
    delete_ref_tag_result = await Ref_tagService.delete_ref_tag_services(query_db, delete_ref_tag)
    logger.info(delete_ref_tag_result.message)

    return ResponseUtil.success(msg=delete_ref_tag_result.message)


@ref_tagController.get(
    '/{ref_id}', response_model=Ref_tagModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref_tag:query'))]
)
async def query_detail_system_ref_tag(request: Request, ref_id: int, query_db: AsyncSession = Depends(get_db)):
    ref_tag_detail_result = await Ref_tagService.ref_tag_detail_services(query_db, ref_id)
    logger.info(f'获取ref_id为{ref_id}的信息成功')

    return ResponseUtil.success(data=ref_tag_detail_result)


@ref_tagController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_tag:export'))])
@Log(title='文献与标签关联', business_type=BusinessType.EXPORT)
async def export_system_ref_tag_list(
    request: Request,
    ref_tag_page_query: Ref_tagPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    ref_tag_query_result = await Ref_tagService.get_ref_tag_list_services(query_db, ref_tag_page_query, is_page=False)
    ref_tag_export_result = await Ref_tagService.export_ref_tag_list_services(ref_tag_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(ref_tag_export_result))
