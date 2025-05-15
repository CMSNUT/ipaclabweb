from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class AlgoModel(BaseModel):
    """
    算法管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    algo_id: Optional[int] = Field(default=None, description='算法id')
    algo_name: Optional[str] = Field(default=None, description='算法名称')
    algo_type: Optional[str] = Field(default=None, description='算法类别')
    algo_lang: Optional[str] = Field(default=None, description='算法语言')
    algo_content: Optional[str] = Field(default=None, description='算法详情')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='algo_name', message='算法名称不能为空')
    def get_algo_name(self):
        return self.algo_name


    def validate_fields(self):
        self.get_algo_name()




class AlgoQueryModel(AlgoModel):
    """
    算法管理不分页查询模型
    """
    pass


@as_query
class AlgoPageQueryModel(AlgoQueryModel):
    """
    算法管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAlgoModel(BaseModel):
    """
    删除算法管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    algo_ids: str = Field(description='需要删除的算法id')
