from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class TagModel(BaseModel):
    """
    标签管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: Optional[int] = Field(default=None, description='标签id')
    tag_label: Optional[str] = Field(default=None, description='标签名称')
    tag_value: Optional[str] = Field(default=None, description='标签值')
    parent_id: Optional[int] = Field(default=None, description='父标签id')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='tag_label', message='标签名称不能为空')
    def get_tag_label(self):
        return self.tag_label

    @NotBlank(field_name='tag_value', message='标签值不能为空')
    def get_tag_value(self):
        return self.tag_value


    def validate_fields(self):
        self.get_tag_label()
        self.get_tag_value()




class TagQueryModel(TagModel):
    """
    标签管理不分页查询模型
    """
    pass


@as_query
class TagPageQueryModel(TagQueryModel):
    """
    标签管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTagModel(BaseModel):
    """
    删除标签管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    tag_ids: str = Field(description='需要删除的标签id')
