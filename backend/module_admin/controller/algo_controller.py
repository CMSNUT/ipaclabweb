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
from module_admin.service.algo_service import AlgoService
from module_admin.entity.vo.algo_vo import DeleteAlgoModel, AlgoModel, AlgoPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


algoController = APIRouter(prefix='/system/algo', dependencies=[Depends(LoginService.get_current_user)])


@algoController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:algo:list'))]
)
async def get_system_algo_list(
    request: Request,
algo_page_query: AlgoPageQueryModel = Depends(AlgoPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    algo_page_query_result = await AlgoService.get_algo_list_services(query_db, algo_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=algo_page_query_result)


@algoController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:algo:add'))])
@ValidateFields(validate_model='add_algo')
@Log(title='算法管理', business_type=BusinessType.INSERT)
async def add_system_algo(
    request: Request,
    add_algo: AlgoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_algo.create_by = current_user.user.user_name
    add_algo.create_time = datetime.now()
    add_algo.update_by = current_user.user.user_name
    add_algo.update_time = datetime.now()
    add_algo_result = await AlgoService.add_algo_services(query_db, add_algo)
    logger.info(add_algo_result.message)

    return ResponseUtil.success(msg=add_algo_result.message)


@algoController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:algo:edit'))])
@ValidateFields(validate_model='edit_algo')
@Log(title='算法管理', business_type=BusinessType.UPDATE)
async def edit_system_algo(
    request: Request,
    edit_algo: AlgoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_algo.update_by = current_user.user.user_name
    edit_algo.update_time = datetime.now()
    edit_algo_result = await AlgoService.edit_algo_services(query_db, edit_algo)
    logger.info(edit_algo_result.message)

    return ResponseUtil.success(msg=edit_algo_result.message)


@algoController.delete('/{algo_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:algo:remove'))])
@Log(title='算法管理', business_type=BusinessType.DELETE)
async def delete_system_algo(request: Request, algo_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_algo = DeleteAlgoModel(algoIds=algo_ids)
    delete_algo_result = await AlgoService.delete_algo_services(query_db, delete_algo)
    logger.info(delete_algo_result.message)

    return ResponseUtil.success(msg=delete_algo_result.message)


@algoController.get(
    '/{algo_id}', response_model=AlgoModel, dependencies=[Depends(CheckUserInterfaceAuth('system:algo:query'))]
)
async def query_detail_system_algo(request: Request, algo_id: int, query_db: AsyncSession = Depends(get_db)):
    algo_detail_result = await AlgoService.algo_detail_services(query_db, algo_id)
    logger.info(f'获取algo_id为{algo_id}的信息成功')

    return ResponseUtil.success(data=algo_detail_result)


@algoController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:algo:export'))])
@Log(title='算法管理', business_type=BusinessType.EXPORT)
async def export_system_algo_list(
    request: Request,
    algo_page_query: AlgoPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    algo_query_result = await AlgoService.get_algo_list_services(query_db, algo_page_query, is_page=False)
    algo_export_result = await AlgoService.export_algo_list_services(request, algo_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(algo_export_result))
