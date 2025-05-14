from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Project_docModel(BaseModel):
    """
    项目文档表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    doc_id: Optional[int] = Field(default=None, description='文档id')
    doc_name: Optional[str] = Field(default=None, description='文档名称')
    project_id: Optional[int] = Field(default=None, description='文献id')
    doc_desc: Optional[str] = Field(default=None, description='文档简介')
    doc_content: Optional[str] = Field(default=None, description='文档内容')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='doc_name', message='文档名称不能为空')
    def get_doc_name(self):
        return self.doc_name

    @NotBlank(field_name='project_id', message='文献id不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='doc_desc', message='文档简介不能为空')
    def get_doc_desc(self):
        return self.doc_desc


    def validate_fields(self):
        self.get_doc_name()
        self.get_project_id()
        self.get_doc_desc()




class Project_docQueryModel(Project_docModel):
    """
    项目文档不分页查询模型
    """
    pass


@as_query
class Project_docPageQueryModel(Project_docQueryModel):
    """
    项目文档分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProject_docModel(BaseModel):
    """
    删除项目文档模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    doc_ids: str = Field(description='需要删除的文档id')
