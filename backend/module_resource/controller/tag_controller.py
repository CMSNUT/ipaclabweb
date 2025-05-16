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
from module_resource.service.tag_service import TagService
from module_resource.entity.vo.tag_vo import DeleteTagModel, TagModel, TagPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


tagController = APIRouter(prefix='/resource/tag', dependencies=[Depends(LoginService.get_current_user)])


@tagController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('resource:tag:list'))]
)
async def get_resource_tag_list(
    request: Request,
tag_query: TagPageQueryModel = Depends(TagPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    tag_query_result = await TagService.get_tag_list_services(query_db, tag_query)
    logger.info('获取成功')

    return ResponseUtil.success(data=tag_query_result)


@tagController.post('', dependencies=[Depends(CheckUserInterfaceAuth('resource:tag:add'))])
@ValidateFields(validate_model='add_tag')
@Log(title='标签管理', business_type=BusinessType.INSERT)
async def add_resource_tag(
    request: Request,
    add_tag: TagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_tag.create_by = current_user.user.user_name
    add_tag.create_time = datetime.now()
    add_tag.update_by = current_user.user.user_name
    add_tag.update_time = datetime.now()
    add_tag_result = await TagService.add_tag_services(query_db, add_tag)
    logger.info(add_tag_result.message)

    return ResponseUtil.success(msg=add_tag_result.message)


@tagController.put('', dependencies=[Depends(CheckUserInterfaceAuth('resource:tag:edit'))])
@ValidateFields(validate_model='edit_tag')
@Log(title='标签管理', business_type=BusinessType.UPDATE)
async def edit_resource_tag(
    request: Request,
    edit_tag: TagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_tag.update_by = current_user.user.user_name
    edit_tag.update_time = datetime.now()
    edit_tag_result = await TagService.edit_tag_services(query_db, edit_tag)
    logger.info(edit_tag_result.message)

    return ResponseUtil.success(msg=edit_tag_result.message)


@tagController.delete('/{tag_ids}', dependencies=[Depends(CheckUserInterfaceAuth('resource:tag:remove'))])
@Log(title='标签管理', business_type=BusinessType.DELETE)
async def delete_resource_tag(request: Request, tag_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_tag = DeleteTagModel(tagIds=tag_ids)
    delete_tag_result = await TagService.delete_tag_services(query_db, delete_tag)
    logger.info(delete_tag_result.message)

    return ResponseUtil.success(msg=delete_tag_result.message)


@tagController.get(
    '/{tag_id}', response_model=TagModel, dependencies=[Depends(CheckUserInterfaceAuth('resource:tag:query'))]
)
async def query_detail_resource_tag(request: Request, tag_id: int, query_db: AsyncSession = Depends(get_db)):
    tag_detail_result = await TagService.tag_detail_services(query_db, tag_id)
    logger.info(f'获取tag_id为{tag_id}的信息成功')

    return ResponseUtil.success(data=tag_detail_result)


@tagController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('resource:tag:export'))])
@Log(title='标签管理', business_type=BusinessType.EXPORT)
async def export_resource_tag_list(
    request: Request,
    tag_page_query: TagPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    tag_query_result = await TagService.get_tag_list_services(query_db, tag_page_query, is_page=False)
    tag_export_result = await TagService.export_tag_list_services(tag_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(tag_export_result))
