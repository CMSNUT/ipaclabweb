from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class AlgoModel(BaseModel):
    """
    程序管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    algo_id: Optional[int] = Field(default=None, description='程序ID')
    algo_name: Optional[str] = Field(default=None, description='程序名称')
    algo_desc: Optional[str] = Field(default=None, description='程序介绍')
    algo_type: Optional[str] = Field(default=None, description='程序类型')
    algo_lang: Optional[str] = Field(default=None, description='编程语言')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='algo_name', message='程序名称不能为空')
    def get_algo_name(self):
        return self.algo_name

    @NotBlank(field_name='algo_type', message='程序类型不能为空')
    def get_algo_type(self):
        return self.algo_type

    @NotBlank(field_name='algo_lang', message='编程语言不能为空')
    def get_algo_lang(self):
        return self.algo_lang


    def validate_fields(self):
        self.get_algo_name()
        self.get_algo_type()
        self.get_algo_lang()




class AlgoQueryModel(AlgoModel):
    """
    程序管理不分页查询模型
    """
    pass


@as_query
class AlgoPageQueryModel(AlgoQueryModel):
    """
    程序管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAlgoModel(BaseModel):
    """
    删除程序管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    algo_ids: str = Field(description='需要删除的程序ID')
