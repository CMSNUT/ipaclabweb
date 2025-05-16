from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, Request, UploadFile
from module_admin.service.common_service import CommonService
from module_admin.service.login_service import LoginService
from utils.log_util import logger
from utils.response_util import ResponseUtil

commonController = APIRouter(prefix='/common', dependencies=[Depends(LoginService.get_current_user)])


@commonController.post('/upload')
async def common_upload(request: Request, file: UploadFile = File(...)):
    upload_result = await CommonService.upload_service(request, file)
    logger.info('上传成功')

    return ResponseUtil.success(model_content=upload_result.result)

# 新增删除路由
@commonController.delete('/delete')
async def common_delete(request: Request, file_name: str = Query(alias='fileName')):
    delete_result = await CommonService.delete_service(file_name)
    if delete_result:
        logger.info('删除成功')
        return ResponseUtil.success(message='删除成功')
    else:
        logger.info('删除失败')
        return ResponseUtil.error(message='删除失败')


@commonController.get('/download')
async def common_download(
    request: Request,
    background_tasks: BackgroundTasks,
    file_name: str = Query(alias='fileName'),
    delete: bool = Query(),
):
    download_result = await CommonService.download_services(background_tasks, file_name, delete)
    logger.info(download_result.message)

    return ResponseUtil.streaming(data=download_result.result)


@commonController.get('/download/resource')
async def common_download_resource(request: Request, resource: str = Query()):
    download_resource_result = await CommonService.download_resource_services(resource)
    logger.info(download_resource_result.message)

    return ResponseUtil.streaming(data=download_resource_result.result)
