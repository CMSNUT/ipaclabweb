from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.env import AppConfig
from config.get_db import init_create_table
from config.get_redis import RedisUtil
from config.get_scheduler import SchedulerUtil
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware
from module_admin.controller.cache_controller import cacheController
from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.common_controller import commonController
from module_admin.controller.config_controller import configController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.log_controller import logController
from module_admin.controller.login_controller import loginController
from module_admin.controller.job_controller import jobController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.notice_controller import noticeController
from module_admin.controller.online_controller import onlineController
from module_admin.controller.post_controler import postController
from module_admin.controller.role_controller import roleController
from module_admin.controller.server_controller import serverController
from module_admin.controller.user_controller import userController
from module_generator.controller.gen_controller import genController
from sub_applications.handle import handle_sub_applications
from utils.common_util import worship
from utils.log_util import logger

from module_admin.controller.tag_controller import tagController
from module_admin.controller.device_controller import deviceController
from module_admin.controller.device_tutorial_controller import device_tutorialController
from module_admin.controller.algo_controller import algoController
from module_admin.controller.algo_tag_controller import algo_tagController
from module_admin.controller.algo_tutorial_controller import algo_tutorialController
from module_admin.controller.dataset_controller import datasetController
from module_admin.controller.dataset_tag_controller import dataset_tagController
from module_admin.controller.project_controller import projectController
from module_admin.controller.project_doc_controller import project_docController
from module_admin.controller.project_member_controller import project_memberController
from module_admin.controller.project_tag_controller import project_tagController
from module_admin.controller.ref_controller import refController
from module_admin.controller.ref_article_controller import ref_articleController
from module_admin.controller.ref_reprod_controller import ref_reprodController
from module_admin.controller.ref_tag_controller import ref_tagController



# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'{AppConfig.app_name}开始启动')
    worship()
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    await RedisUtil.init_sys_dict(app.state.redis)
    await RedisUtil.init_sys_config(app.state.redis)
    await SchedulerUtil.init_system_scheduler()
    logger.info(f'{AppConfig.app_name}启动成功')
    yield
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()


# 初始化FastAPI对象
app = FastAPI(
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    lifespan=lifespan,
)

# 挂载子应用
handle_sub_applications(app)
# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)


# 加载路由列表
controller_list = [
    {'router': loginController, 'tags': ['登录模块']},
    {'router': captchaController, 'tags': ['验证码模块']},
    {'router': userController, 'tags': ['系统管理-用户管理']},
    {'router': roleController, 'tags': ['系统管理-角色管理']},
    {'router': menuController, 'tags': ['系统管理-菜单管理']},
    {'router': deptController, 'tags': ['系统管理-部门管理']},
    {'router': postController, 'tags': ['系统管理-岗位管理']},
    {'router': dictController, 'tags': ['系统管理-字典管理']},
    {'router': configController, 'tags': ['系统管理-参数管理']},
    {'router': noticeController, 'tags': ['系统管理-通知公告管理']},
    {'router': logController, 'tags': ['系统管理-日志管理']},
    {'router': onlineController, 'tags': ['系统监控-在线用户']},
    {'router': jobController, 'tags': ['系统监控-定时任务']},
    {'router': serverController, 'tags': ['系统监控-菜单管理']},
    {'router': cacheController, 'tags': ['系统监控-缓存监控']},
    {'router': commonController, 'tags': ['通用模块']},
    {'router': genController, 'tags': ['代码生成']},

    {'router': tagController, 'tags': ['系统管理-标签管理']},
    {'router': deviceController, 'tags': ['系统管理-仪器设备管理']},
    {'router': device_tutorialController, 'tags': ['系统管理-仪器设备教程']},
    {'router': algoController, 'tags': ['系统管理-算法程序管理']},
    {'router': algo_tagController, 'tags': ['系统管理-算法程序标签']},
    {'router': algo_tutorialController, 'tags': ['系统管理-算法程序教程']},
    {'router': datasetController, 'tags': ['系统管理-数据集管理']},
    {'router': dataset_tagController, 'tags': ['系统管理-数据集标签']},
    {'router': refController, 'tags': ['系统管理-文献管理']},
    {'router': ref_articleController, 'tags': ['系统管理-文献分析']},
    {'router': ref_reprodController, 'tags': ['系统管理-文献复现']},
    {'router': ref_tagController, 'tags': ['系统管理-文献标签']},
    {'router': projectController, 'tags': ['系统管理-项目管理']},
    {'router': project_tagController, 'tags': ['系统管理-项目标签']},
    {'router': project_memberController, 'tags': ['系统管理-项目成员']},
    {'router': project_docController, 'tags': ['系统管理-项目文档']},
]

for controller in controller_list:
    app.include_router(router=controller.get('router'), tags=controller.get('tags'))
