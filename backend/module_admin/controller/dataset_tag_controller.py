from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.dataset_tag_service import Dataset_tagService
from module_admin.entity.vo.dataset_tag_vo import DeleteDataset_tagModel, Dataset_tagModel, Dataset_tagPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


dataset_tagController = APIRouter(prefix='/system/dataset_tag', dependencies=[Depends(LoginService.get_current_user)])


@dataset_tagController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dataset_tag:list'))]
)
async def get_system_dataset_tag_list(
    request: Request,
dataset_tag_page_query: Dataset_tagPageQueryModel = Depends(Dataset_tagPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    dataset_tag_page_query_result = await Dataset_tagService.get_dataset_tag_list_services(query_db, dataset_tag_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=dataset_tag_page_query_result)


@dataset_tagController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset_tag:add'))])
@ValidateFields(validate_model='add_dataset_tag')
@Log(title='数据与标签关联', business_type=BusinessType.INSERT)
async def add_system_dataset_tag(
    request: Request,
    add_dataset_tag: Dataset_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dataset_tag_result = await Dataset_tagService.add_dataset_tag_services(query_db, add_dataset_tag)
    logger.info(add_dataset_tag_result.message)

    return ResponseUtil.success(msg=add_dataset_tag_result.message)


@dataset_tagController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset_tag:edit'))])
@ValidateFields(validate_model='edit_dataset_tag')
@Log(title='数据与标签关联', business_type=BusinessType.UPDATE)
async def edit_system_dataset_tag(
    request: Request,
    edit_dataset_tag: Dataset_tagModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_dataset_tag.update_by = current_user.user.user_name
    edit_dataset_tag.update_time = datetime.now()
    edit_dataset_tag_result = await Dataset_tagService.edit_dataset_tag_services(query_db, edit_dataset_tag)
    logger.info(edit_dataset_tag_result.message)

    return ResponseUtil.success(msg=edit_dataset_tag_result.message)


@dataset_tagController.delete('/{dataset_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset_tag:remove'))])
@Log(title='数据与标签关联', business_type=BusinessType.DELETE)
async def delete_system_dataset_tag(request: Request, dataset_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_dataset_tag = DeleteDataset_tagModel(datasetIds=dataset_ids)
    delete_dataset_tag_result = await Dataset_tagService.delete_dataset_tag_services(query_db, delete_dataset_tag)
    logger.info(delete_dataset_tag_result.message)

    return ResponseUtil.success(msg=delete_dataset_tag_result.message)


@dataset_tagController.get(
    '/{dataset_id}', response_model=Dataset_tagModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dataset_tag:query'))]
)
async def query_detail_system_dataset_tag(request: Request, dataset_id: int, query_db: AsyncSession = Depends(get_db)):
    dataset_tag_detail_result = await Dataset_tagService.dataset_tag_detail_services(query_db, dataset_id)
    logger.info(f'获取dataset_id为{dataset_id}的信息成功')

    return ResponseUtil.success(data=dataset_tag_detail_result)


@dataset_tagController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:dataset_tag:export'))])
@Log(title='数据与标签关联', business_type=BusinessType.EXPORT)
async def export_system_dataset_tag_list(
    request: Request,
    dataset_tag_page_query: Dataset_tagPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    dataset_tag_query_result = await Dataset_tagService.get_dataset_tag_list_services(query_db, dataset_tag_page_query, is_page=False)
    dataset_tag_export_result = await Dataset_tagService.export_dataset_tag_list_services(dataset_tag_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(dataset_tag_export_result))
