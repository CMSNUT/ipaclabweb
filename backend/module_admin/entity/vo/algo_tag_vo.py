from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Algo_tagModel(BaseModel):
    """
    算法与标签关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    algo_id: Optional[int] = Field(default=None, description='算法ID')
    tag_id: Optional[int] = Field(default=None, description='标签ID')






class Algo_tagQueryModel(Algo_tagModel):
    """
    算法与标签关联不分页查询模型
    """
    pass


@as_query
class Algo_tagPageQueryModel(Algo_tagQueryModel):
    """
    算法与标签关联分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAlgo_tagModel(BaseModel):
    """
    删除算法与标签关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    algo_ids: str = Field(description='需要删除的算法ID')
