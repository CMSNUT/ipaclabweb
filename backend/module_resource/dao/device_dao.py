from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_resource.entity.do.device_do import ResDevice
from module_resource.entity.vo.device_vo import DeviceModel, DevicePageQueryModel
from utils.page_util import PageUtil


class DeviceDao:
    """
    仪器管理模块数据库操作层
    """

    @classmethod
    async def get_device_detail_by_id(cls, db: AsyncSession, device_id: int):
        """
        根据仪器id获取仪器管理详细信息

        :param db: orm对象
        :param device_id: 仪器id
        :return: 仪器管理信息对象
        """
        device_info = (
            (
                await db.execute(
                    select(ResDevice)
                    .where(
                        ResDevice.device_id == device_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return device_info

    @classmethod
    async def get_device_detail_by_info(cls, db: AsyncSession, device: DeviceModel):
        """
        根据仪器管理参数获取仪器管理信息

        :param db: orm对象
        :param device: 仪器管理参数对象
        :return: 仪器管理信息对象
        """
        device_info = (
            (
                await db.execute(
                    select(ResDevice).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return device_info

    @classmethod
    async def get_device_list(cls, db: AsyncSession, query_object: DevicePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取仪器管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 仪器管理列表信息对象
        """
        query = (
            select(ResDevice)
            .where(
                ResDevice.device_name.like(f'%{query_object.device_name}%') if query_object.device_name else True,
            )
            .order_by(ResDevice.device_id)
            .distinct()
        )
        device_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return device_list

    @classmethod
    async def add_device_dao(cls, db: AsyncSession, device: DeviceModel):
        """
        新增仪器管理数据库操作

        :param db: orm对象
        :param device: 仪器管理对象
        :return:
        """
        db_device = ResDevice(**device.model_dump(exclude={}))
        db.add(db_device)
        await db.flush()

        return db_device

    @classmethod
    async def edit_device_dao(cls, db: AsyncSession, device: dict):
        """
        编辑仪器管理数据库操作

        :param db: orm对象
        :param device: 需要更新的仪器管理字典
        :return:
        """
        await db.execute(update(ResDevice), [device])

    @classmethod
    async def delete_device_dao(cls, db: AsyncSession, device: DeviceModel):
        """
        删除仪器管理数据库操作

        :param db: orm对象
        :param device: 仪器管理对象
        :return:
        """
        await db.execute(delete(ResDevice).where(ResDevice.device_id.in_([device.device_id])))

