from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class DatasetModel(BaseModel):
    """
    数据管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    dataset_id: Optional[int] = Field(default=None, description='数据id')
    dataset_name: Optional[str] = Field(default=None, description='数据名称')
    dataset_desc: Optional[str] = Field(default=None, description='数据简介')
    dataset_content: Optional[str] = Field(default=None, description='数据详情')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='dataset_name', message='数据名称不能为空')
    def get_dataset_name(self):
        return self.dataset_name


    def validate_fields(self):
        self.get_dataset_name()




class DatasetQueryModel(DatasetModel):
    """
    数据管理不分页查询模型
    """
    pass


@as_query
class DatasetPageQueryModel(DatasetQueryModel):
    """
    数据管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDatasetModel(BaseModel):
    """
    删除数据管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    dataset_ids: str = Field(description='需要删除的数据id')
