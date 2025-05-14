from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.project_tag_service import Project_tagService
from module_admin.entity.vo.project_tag_vo import DeleteProject_tagModel, Project_tagModel, Project_tagPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


project_tagController = APIRouter(prefix='/system/project_tag', dependencies=[Depends(LoginService.get_current_user)])


@project_tagController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:project_tag:list'))]
)
async def get_system_project_tag_list(
    request: Request,
project_tag_page_query: Project_tagPageQueryModel = Depends(Project_tagPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    project_tag_page_query_result = await Project_tagService.get_project_tag_list_services(query_db, project_tag_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=project_tag_page_query_result)


@project_tagController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:project_tag:add'))])
@ValidateFields(validate_model='add_project_tag')
@Log(title='数据与标签关联', business_type=BusinessType.INSERT)
async def add_system_project_tag(
    request: Request,
    add_project_tag: Project_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_project_tag_result = await Project_tagService.add_project_tag_services(query_db, add_project_tag)
    logger.info(add_project_tag_result.message)

    return ResponseUtil.success(msg=add_project_tag_result.message)


@project_tagController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:project_tag:edit'))])
@ValidateFields(validate_model='edit_project_tag')
@Log(title='数据与标签关联', business_type=BusinessType.UPDATE)
async def edit_system_project_tag(
    request: Request,
    edit_project_tag: Project_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_project_tag.update_by = current_user.user.user_name
    edit_project_tag.update_time = datetime.now()
    edit_project_tag_result = await Project_tagService.edit_project_tag_services(query_db, edit_project_tag)
    logger.info(edit_project_tag_result.message)

    return ResponseUtil.success(msg=edit_project_tag_result.message)


@project_tagController.delete('/{project_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:project_tag:remove'))])
@Log(title='数据与标签关联', business_type=BusinessType.DELETE)
async def delete_system_project_tag(request: Request, project_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_project_tag = DeleteProject_tagModel(projectIds=project_ids)
    delete_project_tag_result = await Project_tagService.delete_project_tag_services(query_db, delete_project_tag)
    logger.info(delete_project_tag_result.message)

    return ResponseUtil.success(msg=delete_project_tag_result.message)


@project_tagController.get(
    '/{project_id}', response_model=Project_tagModel, dependencies=[Depends(CheckUserInterfaceAuth('system:project_tag:query'))]
)
async def query_detail_system_project_tag(request: Request, project_id: int, query_db: AsyncSession = Depends(get_db)):
    project_tag_detail_result = await Project_tagService.project_tag_detail_services(query_db, project_id)
    logger.info(f'获取project_id为{project_id}的信息成功')

    return ResponseUtil.success(data=project_tag_detail_result)


@project_tagController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:project_tag:export'))])
@Log(title='数据与标签关联', business_type=BusinessType.EXPORT)
async def export_system_project_tag_list(
    request: Request,
    project_tag_page_query: Project_tagPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    project_tag_query_result = await Project_tagService.get_project_tag_list_services(query_db, project_tag_page_query, is_page=False)
    project_tag_export_result = await Project_tagService.export_project_tag_list_services(project_tag_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(project_tag_export_result))
