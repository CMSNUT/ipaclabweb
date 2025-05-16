from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Algo_tagModel(BaseModel):
    """
    程序标签关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    algo_id: Optional[int] = Field(default=None, description='程序ID')
    tag_id: Optional[int] = Field(default=None, description='标签ID')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='algo_id', message='程序ID不能为空')
    def get_algo_id(self):
        return self.algo_id

    @NotBlank(field_name='tag_id', message='标签ID不能为空')
    def get_tag_id(self):
        return self.tag_id


    def validate_fields(self):
        self.get_algo_id()
        self.get_tag_id()




class Algo_tagQueryModel(Algo_tagModel):
    """
    程序标签关联不分页查询模型
    """
    pass


@as_query
class Algo_tagPageQueryModel(Algo_tagQueryModel):
    """
    程序标签关联分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAlgo_tagModel(BaseModel):
    """
    删除程序标签关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    algo_ids: str = Field(description='需要删除的程序ID')
