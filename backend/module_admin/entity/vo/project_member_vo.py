from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Project_memberModel(BaseModel):
    """
    项目与用户关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    project_id: Optional[int] = Field(default=None, description='数据ID')
    user_id: Optional[int] = Field(default=None, description='标签ID')
    member_role: Optional[str] = Field(default=None, description='项目分工')






class Project_memberQueryModel(Project_memberModel):
    """
    项目与用户关联不分页查询模型
    """
    pass


@as_query
class Project_memberPageQueryModel(Project_memberQueryModel):
    """
    项目与用户关联分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProject_memberModel(BaseModel):
    """
    删除项目与用户关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    project_ids: str = Field(description='需要删除的数据ID')
