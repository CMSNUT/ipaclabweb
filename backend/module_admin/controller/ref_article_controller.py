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
from module_admin.service.ref_article_service import Ref_articleService
from module_admin.entity.vo.ref_article_vo import DeleteRef_articleModel, Ref_articleModel, Ref_articlePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


ref_articleController = APIRouter(prefix='/system/ref_article', dependencies=[Depends(LoginService.get_current_user)])


@ref_articleController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref_article:list'))]
)
async def get_system_ref_article_list(
    request: Request,
ref_article_page_query: Ref_articlePageQueryModel = Depends(Ref_articlePageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    ref_article_page_query_result = await Ref_articleService.get_ref_article_list_services(query_db, ref_article_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=ref_article_page_query_result)


@ref_articleController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_article:add'))])
@ValidateFields(validate_model='add_ref_article')
@Log(title='文献分析', business_type=BusinessType.INSERT)
async def add_system_ref_article(
    request: Request,
    add_ref_article: Ref_articleModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_ref_article.create_by = current_user.user.user_name
    add_ref_article.create_time = datetime.now()
    add_ref_article.update_by = current_user.user.user_name
    add_ref_article.update_time = datetime.now()
    add_ref_article_result = await Ref_articleService.add_ref_article_services(query_db, add_ref_article)
    logger.info(add_ref_article_result.message)

    return ResponseUtil.success(msg=add_ref_article_result.message)


@ref_articleController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_article:edit'))])
@ValidateFields(validate_model='edit_ref_article')
@Log(title='文献分析', business_type=BusinessType.UPDATE)
async def edit_system_ref_article(
    request: Request,
    edit_ref_article: Ref_articleModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_ref_article.update_by = current_user.user.user_name
    edit_ref_article.update_time = datetime.now()
    edit_ref_article_result = await Ref_articleService.edit_ref_article_services(query_db, edit_ref_article)
    logger.info(edit_ref_article_result.message)

    return ResponseUtil.success(msg=edit_ref_article_result.message)


@ref_articleController.delete('/{article_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_article:remove'))])
@Log(title='文献分析', business_type=BusinessType.DELETE)
async def delete_system_ref_article(request: Request, article_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_ref_article = DeleteRef_articleModel(articleIds=article_ids)
    delete_ref_article_result = await Ref_articleService.delete_ref_article_services(query_db, delete_ref_article)
    logger.info(delete_ref_article_result.message)

    return ResponseUtil.success(msg=delete_ref_article_result.message)


@ref_articleController.get(
    '/{article_id}', response_model=Ref_articleModel, dependencies=[Depends(CheckUserInterfaceAuth('system:ref_article:query'))]
)
async def query_detail_system_ref_article(request: Request, article_id: int, query_db: AsyncSession = Depends(get_db)):
    ref_article_detail_result = await Ref_articleService.ref_article_detail_services(query_db, article_id)
    logger.info(f'获取article_id为{article_id}的信息成功')

    return ResponseUtil.success(data=ref_article_detail_result)


@ref_articleController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:ref_article:export'))])
@Log(title='文献分析', business_type=BusinessType.EXPORT)
async def export_system_ref_article_list(
    request: Request,
    ref_article_page_query: Ref_articlePageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    ref_article_query_result = await Ref_articleService.get_ref_article_list_services(query_db, ref_article_page_query, is_page=False)
    ref_article_export_result = await Ref_articleService.export_ref_article_list_services(ref_article_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(ref_article_export_result))
