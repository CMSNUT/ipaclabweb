from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Project_tagModel(BaseModel):
    """
    数据与标签关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    project_id: Optional[int] = Field(default=None, description='项目ID')
    tag_id: Optional[int] = Field(default=None, description='标签ID')






class Project_tagQueryModel(Project_tagModel):
    """
    数据与标签关联不分页查询模型
    """
    pass


@as_query
class Project_tagPageQueryModel(Project_tagQueryModel):
    """
    数据与标签关联分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProject_tagModel(BaseModel):
    """
    删除数据与标签关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    project_ids: str = Field(description='需要删除的项目ID')
