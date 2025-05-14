from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Ref_reprodModel(BaseModel):
    """
    文献复现表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    reprod_id: Optional[int] = Field(default=None, description='复现id')
    reprod_name: Optional[str] = Field(default=None, description='复现名称')
    ref_id: Optional[int] = Field(default=None, description='文献id')
    reprod_content: Optional[str] = Field(default=None, description='复现内容')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='reprod_name', message='复现名称不能为空')
    def get_reprod_name(self):
        return self.reprod_name

    @NotBlank(field_name='ref_id', message='文献id不能为空')
    def get_ref_id(self):
        return self.ref_id


    def validate_fields(self):
        self.get_reprod_name()
        self.get_ref_id()




class Ref_reprodQueryModel(Ref_reprodModel):
    """
    文献复现不分页查询模型
    """
    pass


@as_query
class Ref_reprodPageQueryModel(Ref_reprodQueryModel):
    """
    文献复现分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteRef_reprodModel(BaseModel):
    """
    删除文献复现模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    reprod_ids: str = Field(description='需要删除的复现id')
