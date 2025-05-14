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
from module_admin.service.dataset_service import DatasetService
from module_admin.entity.vo.dataset_vo import DeleteDatasetModel, DatasetModel, DatasetPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


datasetController = APIRouter(prefix='/system/dataset', dependencies=[Depends(LoginService.get_current_user)])


@datasetController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dataset:list'))]
)
async def get_system_dataset_list(
    request: Request,
dataset_page_query: DatasetPageQueryModel = Depends(DatasetPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    dataset_page_query_result = await DatasetService.get_dataset_list_services(query_db, dataset_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=dataset_page_query_result)


@datasetController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset:add'))])
@ValidateFields(validate_model='add_dataset')
@Log(title='数据管理', business_type=BusinessType.INSERT)
async def add_system_dataset(
    request: Request,
    add_dataset: DatasetModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dataset.create_by = current_user.user.user_name
    add_dataset.create_time = datetime.now()
    add_dataset.update_by = current_user.user.user_name
    add_dataset.update_time = datetime.now()
    add_dataset_result = await DatasetService.add_dataset_services(query_db, add_dataset)
    logger.info(add_dataset_result.message)

    return ResponseUtil.success(msg=add_dataset_result.message)


@datasetController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset:edit'))])
@ValidateFields(validate_model='edit_dataset')
@Log(title='数据管理', business_type=BusinessType.UPDATE)
async def edit_system_dataset(
    request: Request,
    edit_dataset: DatasetModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_dataset.update_by = current_user.user.user_name
    edit_dataset.update_time = datetime.now()
    edit_dataset_result = await DatasetService.edit_dataset_services(query_db, edit_dataset)
    logger.info(edit_dataset_result.message)

    return ResponseUtil.success(msg=edit_dataset_result.message)


@datasetController.delete('/{dataset_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset:remove'))])
@Log(title='数据管理', business_type=BusinessType.DELETE)
async def delete_system_dataset(request: Request, dataset_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_dataset = DeleteDatasetModel(datasetIds=dataset_ids)
    delete_dataset_result = await DatasetService.delete_dataset_services(query_db, delete_dataset)
    logger.info(delete_dataset_result.message)

    return ResponseUtil.success(msg=delete_dataset_result.message)


@datasetController.get(
    '/{dataset_id}', response_model=DatasetModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dataset:query'))]
)
async def query_detail_system_dataset(request: Request, dataset_id: int, query_db: AsyncSession = Depends(get_db)):
    dataset_detail_result = await DatasetService.dataset_detail_services(query_db, dataset_id)
    logger.info(f'获取dataset_id为{dataset_id}的信息成功')

    return ResponseUtil.success(data=dataset_detail_result)


@datasetController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset:export'))])
@Log(title='数据管理', business_type=BusinessType.EXPORT)
async def export_system_dataset_list(
    request: Request,
    dataset_page_query: DatasetPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    dataset_query_result = await DatasetService.get_dataset_list_services(query_db, dataset_page_query, is_page=False)
    dataset_export_result = await DatasetService.export_dataset_list_services(dataset_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(dataset_export_result))
