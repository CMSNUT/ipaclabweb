from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.project_member_service import Project_memberService
from module_admin.entity.vo.project_member_vo import DeleteProject_memberModel, Project_memberModel, Project_memberPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


project_memberController = APIRouter(prefix='/system/project_member', dependencies=[Depends(LoginService.get_current_user)])


@project_memberController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:project_member:list'))]
)
async def get_system_project_member_list(
    request: Request,
project_member_page_query: Project_memberPageQueryModel = Depends(Project_memberPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    project_member_page_query_result = await Project_memberService.get_project_member_list_services(query_db, project_member_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=project_member_page_query_result)


@project_memberController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:project_member:add'))])
@ValidateFields(validate_model='add_project_member')
@Log(title='项目与用户关联', business_type=BusinessType.INSERT)
async def add_system_project_member(
    request: Request,
    add_project_member: Project_memberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_project_member_result = await Project_memberService.add_project_member_services(query_db, add_project_member)
    logger.info(add_project_member_result.message)

    return ResponseUtil.success(msg=add_project_member_result.message)


@project_memberController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:project_member:edit'))])
@ValidateFields(validate_model='edit_project_member')
@Log(title='项目与用户关联', business_type=BusinessType.UPDATE)
async def edit_system_project_member(
    request: Request,
    edit_project_member: Project_memberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_project_member.update_by = current_user.user.user_name
    edit_project_member.update_time = datetime.now()
    edit_project_member_result = await Project_memberService.edit_project_member_services(query_db, edit_project_member)
    logger.info(edit_project_member_result.message)

    return ResponseUtil.success(msg=edit_project_member_result.message)


@project_memberController.delete('/{project_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:project_member:remove'))])
@Log(title='项目与用户关联', business_type=BusinessType.DELETE)
async def delete_system_project_member(request: Request, project_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_project_member = DeleteProject_memberModel(projectIds=project_ids)
    delete_project_member_result = await Project_memberService.delete_project_member_services(query_db, delete_project_member)
    logger.info(delete_project_member_result.message)

    return ResponseUtil.success(msg=delete_project_member_result.message)


@project_memberController.get(
    '/{project_id}', response_model=Project_memberModel, dependencies=[Depends(CheckUserInterfaceAuth('system:project_member:query'))]
)
async def query_detail_system_project_member(request: Request, project_id: int, query_db: AsyncSession = Depends(get_db)):
    project_member_detail_result = await Project_memberService.project_member_detail_services(query_db, project_id)
    logger.info(f'获取project_id为{project_id}的信息成功')

    return ResponseUtil.success(data=project_member_detail_result)


@project_memberController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:project_member:export'))])
@Log(title='项目与用户关联', business_type=BusinessType.EXPORT)
async def export_system_project_member_list(
    request: Request,
    project_member_page_query: Project_memberPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    project_member_query_result = await Project_memberService.get_project_member_list_services(query_db, project_member_page_query, is_page=False)
    project_member_export_result = await Project_memberService.export_project_member_list_services(project_member_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(project_member_export_result))
