from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class RefModel(BaseModel):
    """
    文献管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    ref_id: Optional[int] = Field(default=None, description='文献id')
    ref_title: Optional[str] = Field(default=None, description='文献英文标题')
    ref_title_zh: Optional[str] = Field(default=None, description='文献中文标题')
    ref_doi: Optional[str] = Field(default=None, description='文献DOI')
    ref_abs: Optional[str] = Field(default=None, description='文献摘要')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='ref_title', message='文献英文标题不能为空')
    def get_ref_title(self):
        return self.ref_title


    def validate_fields(self):
        self.get_ref_title()




class RefQueryModel(RefModel):
    """
    文献管理不分页查询模型
    """
    pass


@as_query
class RefPageQueryModel(RefQueryModel):
    """
    文献管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteRefModel(BaseModel):
    """
    删除文献管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ref_ids: str = Field(description='需要删除的文献id')
