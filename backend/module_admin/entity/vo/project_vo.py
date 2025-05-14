from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class ProjectModel(BaseModel):
    """
    项目管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    project_id: Optional[int] = Field(default=None, description='项目id')
    project_title: Optional[str] = Field(default=None, description='项目标题')
    user_id: Optional[int] = Field(default=None, description='项目负责人')
    project_desc: Optional[str] = Field(default=None, description='项目描述')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='project_title', message='项目标题不能为空')
    def get_project_title(self):
        return self.project_title

    @NotBlank(field_name='user_id', message='项目负责人不能为空')
    def get_user_id(self):
        return self.user_id


    def validate_fields(self):
        self.get_project_title()
        self.get_user_id()




class ProjectQueryModel(ProjectModel):
    """
    项目管理不分页查询模型
    """
    pass


@as_query
class ProjectPageQueryModel(ProjectQueryModel):
    """
    项目管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProjectModel(BaseModel):
    """
    删除项目管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    project_ids: str = Field(description='需要删除的项目id')
