from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.dataset_do import SysDataset
from module_admin.entity.vo.dataset_vo import DatasetModel, DatasetPageQueryModel
from utils.page_util import PageUtil


class DatasetDao:
    """
    数据管理模块数据库操作层
    """

    @classmethod
    async def get_dataset_detail_by_id(cls, db: AsyncSession, dataset_id: int):
        """
        根据数据id获取数据管理详细信息

        :param db: orm对象
        :param dataset_id: 数据id
        :return: 数据管理信息对象
        """
        dataset_info = (
            (
                await db.execute(
                    select(SysDataset)
                    .where(
                        SysDataset.dataset_id == dataset_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return dataset_info

    @classmethod
    async def get_dataset_detail_by_info(cls, db: AsyncSession, dataset: DatasetModel):
        """
        根据数据管理参数获取数据管理信息

        :param db: orm对象
        :param dataset: 数据管理参数对象
        :return: 数据管理信息对象
        """
        dataset_info = (
            (
                await db.execute(
                    select(SysDataset).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return dataset_info

    @classmethod
    async def get_dataset_list(cls, db: AsyncSession, query_object: DatasetPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取数据管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据管理列表信息对象
        """
        query = (
            select(SysDataset)
            .where(
                SysDataset.dataset_name.like(f'%{query_object.dataset_name}%') if query_object.dataset_name else True,
                SysDataset.dataset_desc == query_object.dataset_desc if query_object.dataset_desc else True,
                SysDataset.dataset_content.like(f'%{query_object.dataset_content}%') if query_object.dataset_content else True,
            )
            .order_by(SysDataset.dataset_id)
            .distinct()
        )
        dataset_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return dataset_list

    @classmethod
    async def add_dataset_dao(cls, db: AsyncSession, dataset: DatasetModel):
        """
        新增数据管理数据库操作

        :param db: orm对象
        :param dataset: 数据管理对象
        :return:
        """
        db_dataset = SysDataset(**dataset.model_dump(exclude={}))
        db.add(db_dataset)
        await db.flush()

        return db_dataset

    @classmethod
    async def edit_dataset_dao(cls, db: AsyncSession, dataset: dict):
        """
        编辑数据管理数据库操作

        :param db: orm对象
        :param dataset: 需要更新的数据管理字典
        :return:
        """
        await db.execute(update(SysDataset), [dataset])

    @classmethod
    async def delete_dataset_dao(cls, db: AsyncSession, dataset: DatasetModel):
        """
        删除数据管理数据库操作

        :param db: orm对象
        :param dataset: 数据管理对象
        :return:
        """
        await db.execute(delete(SysDataset).where(SysDataset.dataset_id.in_([dataset.dataset_id])))

