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
from module_admin.service.algo_tutorial_service import Algo_tutorialService
from module_admin.entity.vo.algo_tutorial_vo import DeleteAlgo_tutorialModel, Algo_tutorialModel, Algo_tutorialPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


algo_tutorialController = APIRouter(prefix='/system/algo_tutorial', dependencies=[Depends(LoginService.get_current_user)])


@algo_tutorialController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:algo_tutorial:list'))]
)
async def get_system_algo_tutorial_list(
    request: Request,
algo_tutorial_page_query: Algo_tutorialPageQueryModel = Depends(Algo_tutorialPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    algo_tutorial_page_query_result = await Algo_tutorialService.get_algo_tutorial_list_services(query_db, algo_tutorial_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=algo_tutorial_page_query_result)


@algo_tutorialController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:algo_tutorial:add'))])
@ValidateFields(validate_model='add_algo_tutorial')
@Log(title='算法教程', business_type=BusinessType.INSERT)
async def add_system_algo_tutorial(
    request: Request,
    add_algo_tutorial: Algo_tutorialModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_algo_tutorial.create_by = current_user.user.user_name
    add_algo_tutorial.create_time = datetime.now()
    add_algo_tutorial.update_by = current_user.user.user_name
    add_algo_tutorial.update_time = datetime.now()
    add_algo_tutorial_result = await Algo_tutorialService.add_algo_tutorial_services(query_db, add_algo_tutorial)
    logger.info(add_algo_tutorial_result.message)

    return ResponseUtil.success(msg=add_algo_tutorial_result.message)


@algo_tutorialController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:algo_tutorial:edit'))])
@ValidateFields(validate_model='edit_algo_tutorial')
@Log(title='算法教程', business_type=BusinessType.UPDATE)
async def edit_system_algo_tutorial(
    request: Request,
    edit_algo_tutorial: Algo_tutorialModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_algo_tutorial.update_by = current_user.user.user_name
    edit_algo_tutorial.update_time = datetime.now()
    edit_algo_tutorial_result = await Algo_tutorialService.edit_algo_tutorial_services(query_db, edit_algo_tutorial)
    logger.info(edit_algo_tutorial_result.message)

    return ResponseUtil.success(msg=edit_algo_tutorial_result.message)


@algo_tutorialController.delete('/{tutorial_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:algo_tutorial:remove'))])
@Log(title='算法教程', business_type=BusinessType.DELETE)
async def delete_system_algo_tutorial(request: Request, tutorial_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_algo_tutorial = DeleteAlgo_tutorialModel(tutorialIds=tutorial_ids)
    delete_algo_tutorial_result = await Algo_tutorialService.delete_algo_tutorial_services(query_db, delete_algo_tutorial)
    logger.info(delete_algo_tutorial_result.message)

    return ResponseUtil.success(msg=delete_algo_tutorial_result.message)


@algo_tutorialController.get(
    '/{tutorial_id}', response_model=Algo_tutorialModel, dependencies=[Depends(CheckUserInterfaceAuth('system:algo_tutorial:query'))]
)
async def query_detail_system_algo_tutorial(request: Request, tutorial_id: int, query_db: AsyncSession = Depends(get_db)):
    algo_tutorial_detail_result = await Algo_tutorialService.algo_tutorial_detail_services(query_db, tutorial_id)
    logger.info(f'获取tutorial_id为{tutorial_id}的信息成功')

    return ResponseUtil.success(data=algo_tutorial_detail_result)


@algo_tutorialController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:algo_tutorial:export'))])
@Log(title='算法教程', business_type=BusinessType.EXPORT)
async def export_system_algo_tutorial_list(
    request: Request,
    algo_tutorial_page_query: Algo_tutorialPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    algo_tutorial_query_result = await Algo_tutorialService.get_algo_tutorial_list_services(query_db, algo_tutorial_page_query, is_page=False)
    algo_tutorial_export_result = await Algo_tutorialService.export_algo_tutorial_list_services(algo_tutorial_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(algo_tutorial_export_result))
