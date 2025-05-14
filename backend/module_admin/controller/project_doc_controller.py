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
from module_admin.service.project_doc_service import Project_docService
from module_admin.entity.vo.project_doc_vo import DeleteProject_docModel, Project_docModel, Project_docPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


project_docController = APIRouter(prefix='/system/project_doc', dependencies=[Depends(LoginService.get_current_user)])


@project_docController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:project_doc:list'))]
)
async def get_system_project_doc_list(
    request: Request,
project_doc_page_query: Project_docPageQueryModel = Depends(Project_docPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    project_doc_page_query_result = await Project_docService.get_project_doc_list_services(query_db, project_doc_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=project_doc_page_query_result)


@project_docController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:project_doc:add'))])
@ValidateFields(validate_model='add_project_doc')
@Log(title='项目文档', business_type=BusinessType.INSERT)
async def add_system_project_doc(
    request: Request,
    add_project_doc: Project_docModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_project_doc.create_by = current_user.user.user_name
    add_project_doc.create_time = datetime.now()
    add_project_doc.update_by = current_user.user.user_name
    add_project_doc.update_time = datetime.now()
    add_project_doc_result = await Project_docService.add_project_doc_services(query_db, add_project_doc)
    logger.info(add_project_doc_result.message)

    return ResponseUtil.success(msg=add_project_doc_result.message)


@project_docController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:project_doc:edit'))])
@ValidateFields(validate_model='edit_project_doc')
@Log(title='项目文档', business_type=BusinessType.UPDATE)
async def edit_system_project_doc(
    request: Request,
    edit_project_doc: Project_docModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_project_doc.update_by = current_user.user.user_name
    edit_project_doc.update_time = datetime.now()
    edit_project_doc_result = await Project_docService.edit_project_doc_services(query_db, edit_project_doc)
    logger.info(edit_project_doc_result.message)

    return ResponseUtil.success(msg=edit_project_doc_result.message)


@project_docController.delete('/{doc_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:project_doc:remove'))])
@Log(title='项目文档', business_type=BusinessType.DELETE)
async def delete_system_project_doc(request: Request, doc_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_project_doc = DeleteProject_docModel(docIds=doc_ids)
    delete_project_doc_result = await Project_docService.delete_project_doc_services(query_db, delete_project_doc)
    logger.info(delete_project_doc_result.message)

    return ResponseUtil.success(msg=delete_project_doc_result.message)


@project_docController.get(
    '/{doc_id}', response_model=Project_docModel, dependencies=[Depends(CheckUserInterfaceAuth('system:project_doc:query'))]
)
async def query_detail_system_project_doc(request: Request, doc_id: int, query_db: AsyncSession = Depends(get_db)):
    project_doc_detail_result = await Project_docService.project_doc_detail_services(query_db, doc_id)
    logger.info(f'获取doc_id为{doc_id}的信息成功')

    return ResponseUtil.success(data=project_doc_detail_result)


@project_docController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:project_doc:export'))])
@Log(title='项目文档', business_type=BusinessType.EXPORT)
async def export_system_project_doc_list(
    request: Request,
    project_doc_page_query: Project_docPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    project_doc_query_result = await Project_docService.get_project_doc_list_services(query_db, project_doc_page_query, is_page=False)
    project_doc_export_result = await Project_docService.export_project_doc_list_services(project_doc_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(project_doc_export_result))
