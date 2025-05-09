from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.device_tutorial_do import SysDeviceTutorial
from module_admin.entity.vo.device_tutorial_vo import Device_tutorialModel, Device_tutorialPageQueryModel
from utils.page_util import PageUtil


class Device_tutorialDao:
    """
    仪器教程模块数据库操作层
    """

    @classmethod
    async def get_device_tutorial_detail_by_id(cls, db: AsyncSession, tutorial_id: int):
        """
        根据教程ID获取仪器教程详细信息

        :param db: orm对象
        :param tutorial_id: 教程ID
        :return: 仪器教程信息对象
        """
        device_tutorial_info = (
            (
                await db.execute(
                    select(SysDeviceTutorial)
                    .where(
                        SysDeviceTutorial.tutorial_id == tutorial_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return device_tutorial_info

    @classmethod
    async def get_device_tutorial_detail_by_info(cls, db: AsyncSession, device_tutorial: Device_tutorialModel):
        """
        根据仪器教程参数获取仪器教程信息

        :param db: orm对象
        :param device_tutorial: 仪器教程参数对象
        :return: 仪器教程信息对象
        """
        device_tutorial_info = (
            (
                await db.execute(
                    select(SysDeviceTutorial).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return device_tutorial_info

    @classmethod
    async def get_device_tutorial_list(cls, db: AsyncSession, query_object: Device_tutorialPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取仪器教程列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器教程列表信息对象
        """
        query = (
            select(SysDeviceTutorial)
            .where(
                SysDeviceTutorial.device_id.like(f'%{query_object.device_id}%') if query_object.device_id else True,
                SysDeviceTutorial.tutorial_title.like(f'%{query_object.tutorial_title}%') if query_object.tutorial_title else True,
                SysDeviceTutorial.tutorial_category == query_object.tutorial_category if query_object.tutorial_category else True,
            )
            .order_by(SysDeviceTutorial.tutorial_id)
            .distinct()
        )
        device_tutorial_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return device_tutorial_list

    @classmethod
    async def add_device_tutorial_dao(cls, db: AsyncSession, device_tutorial: Device_tutorialModel):
        """
        新增仪器教程数据库操作

        :param db: orm对象
        :param device_tutorial: 仪器教程对象
        :return:
        """
        db_device_tutorial = SysDeviceTutorial(**device_tutorial.model_dump(exclude={}))
        db.add(db_device_tutorial)
        await db.flush()

        return db_device_tutorial

    @classmethod
    async def edit_device_tutorial_dao(cls, db: AsyncSession, device_tutorial: dict):
        """
        编辑仪器教程数据库操作

        :param db: orm对象
        :param device_tutorial: 需要更新的仪器教程字典
        :return:
        """
        await db.execute(update(SysDeviceTutorial), [device_tutorial])

    @classmethod
    async def delete_device_tutorial_dao(cls, db: AsyncSession, device_tutorial: Device_tutorialModel):
        """
        删除仪器教程数据库操作

        :param db: orm对象
        :param device_tutorial: 仪器教程对象
        :return:
        """
        await db.execute(delete(SysDeviceTutorial).where(SysDeviceTutorial.tutorial_id.in_([device_tutorial.tutorial_id])))

