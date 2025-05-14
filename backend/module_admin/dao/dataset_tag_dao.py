from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.dataset_tag_do import SysDatasetTag
from module_admin.entity.vo.dataset_tag_vo import Dataset_tagModel, Dataset_tagPageQueryModel
from utils.page_util import PageUtil


class Dataset_tagDao:
    """
    数据与标签关联模块数据库操作层
    """

    @classmethod
    async def get_dataset_tag_detail_by_id(cls, db: AsyncSession, dataset_id: int):
        """
        根据数据ID获取数据与标签关联详细信息

        :param db: orm对象
        :param dataset_id: 数据ID
        :return: 数据与标签关联信息对象
        """
        dataset_tag_info = (
            (
                await db.execute(
                    select(SysDatasetTag)
                    .where(
                        SysDatasetTag.dataset_id == dataset_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return dataset_tag_info

    @classmethod
    async def get_dataset_tag_detail_by_info(cls, db: AsyncSession, dataset_tag: Dataset_tagModel):
        """
        根据数据与标签关联参数获取数据与标签关联信息

        :param db: orm对象
        :param dataset_tag: 数据与标签关联参数对象
        :return: 数据与标签关联信息对象
        """
        dataset_tag_info = (
            (
                await db.execute(
                    select(SysDatasetTag).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return dataset_tag_info

    @classmethod
    async def get_dataset_tag_list(cls, db: AsyncSession, query_object: Dataset_tagPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取数据与标签关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据与标签关联列表信息对象
        """
        query = (
            select(SysDatasetTag)
            .where(
            )
            .order_by(SysDatasetTag.dataset_id)
            .distinct()
        )
        dataset_tag_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return dataset_tag_list

    @classmethod
    async def add_dataset_tag_dao(cls, db: AsyncSession, dataset_tag: Dataset_tagModel):
        """
        新增数据与标签关联数据库操作

        :param db: orm对象
        :param dataset_tag: 数据与标签关联对象
        :return:
        """
        db_dataset_tag = SysDatasetTag(**dataset_tag.model_dump(exclude={}))
        db.add(db_dataset_tag)
        await db.flush()

        return db_dataset_tag

    @classmethod
    async def edit_dataset_tag_dao(cls, db: AsyncSession, dataset_tag: dict):
        """
        编辑数据与标签关联数据库操作

        :param db: orm对象
        :param dataset_tag: 需要更新的数据与标签关联字典
        :return:
        """
        await db.execute(update(SysDatasetTag), [dataset_tag])

    @classmethod
    async def delete_dataset_tag_dao(cls, db: AsyncSession, dataset_tag: Dataset_tagModel):
        """
        删除数据与标签关联数据库操作

        :param db: orm对象
        :param dataset_tag: 数据与标签关联对象
        :return:
        """
        await db.execute(delete(SysDatasetTag).where(SysDatasetTag.dataset_id.in_([dataset_tag.dataset_id])))

