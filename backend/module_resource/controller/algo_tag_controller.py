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
from module_resource.service.algo_tag_service import Algo_tagService
from module_resource.entity.vo.algo_tag_vo import DeleteAlgo_tagModel, Algo_tagModel, Algo_tagPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


algo_tagController = APIRouter(prefix='/resource/algo_tag', dependencies=[Depends(LoginService.get_current_user)])


@algo_tagController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('resource:algo_tag:list'))]
)
async def get_resource_algo_tag_list(
    request: Request,
algo_tag_page_query: Algo_tagPageQueryModel = Depends(Algo_tagPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    algo_tag_page_query_result = await Algo_tagService.get_algo_tag_list_services(query_db, algo_tag_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=algo_tag_page_query_result)


@algo_tagController.post('', dependencies=[Depends(CheckUserInterfaceAuth('resource:algo_tag:add'))])
@ValidateFields(validate_model='add_algo_tag')
@Log(title='程序标签关联', business_type=BusinessType.INSERT)
async def add_resource_algo_tag(
    request: Request,
    add_algo_tag: Algo_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_algo_tag.create_by = current_user.user.user_name
    add_algo_tag.create_time = datetime.now()
    add_algo_tag.update_by = current_user.user.user_name
    add_algo_tag.update_time = datetime.now()
    add_algo_tag_result = await Algo_tagService.add_algo_tag_services(query_db, add_algo_tag)
    logger.info(add_algo_tag_result.message)

    return ResponseUtil.success(msg=add_algo_tag_result.message)


@algo_tagController.put('', dependencies=[Depends(CheckUserInterfaceAuth('resource:algo_tag:edit'))])
@ValidateFields(validate_model='edit_algo_tag')
@Log(title='程序标签关联', business_type=BusinessType.UPDATE)
async def edit_resource_algo_tag(
    request: Request,
    edit_algo_tag: Algo_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_algo_tag.update_by = current_user.user.user_name
    edit_algo_tag.update_time = datetime.now()
    edit_algo_tag_result = await Algo_tagService.edit_algo_tag_services(query_db, edit_algo_tag)
    logger.info(edit_algo_tag_result.message)

    return ResponseUtil.success(msg=edit_algo_tag_result.message)


@algo_tagController.delete('/{algo_ids}', dependencies=[Depends(CheckUserInterfaceAuth('resource:algo_tag:remove'))])
@Log(title='程序标签关联', business_type=BusinessType.DELETE)
async def delete_resource_algo_tag(request: Request, algo_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_algo_tag = DeleteAlgo_tagModel(algoIds=algo_ids)
    delete_algo_tag_result = await Algo_tagService.delete_algo_tag_services(query_db, delete_algo_tag)
    logger.info(delete_algo_tag_result.message)

    return ResponseUtil.success(msg=delete_algo_tag_result.message)


@algo_tagController.get(
    '/{algo_id}', response_model=Algo_tagModel, dependencies=[Depends(CheckUserInterfaceAuth('resource:algo_tag:query'))]
)
async def query_detail_resource_algo_tag(request: Request, algo_id: int, query_db: AsyncSession = Depends(get_db)):
    algo_tag_detail_result = await Algo_tagService.algo_tag_detail_services(query_db, algo_id)
    logger.info(f'获取algo_id为{algo_id}的信息成功')

    return ResponseUtil.success(data=algo_tag_detail_result)


@algo_tagController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('resource:algo_tag:export'))])
@Log(title='程序标签关联', business_type=BusinessType.EXPORT)
async def export_resource_algo_tag_list(
    request: Request,
    algo_tag_page_query: Algo_tagPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    algo_tag_query_result = await Algo_tagService.get_algo_tag_list_services(query_db, algo_tag_page_query, is_page=False)
    algo_tag_export_result = await Algo_tagService.export_algo_tag_list_services(algo_tag_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(algo_tag_export_result))
