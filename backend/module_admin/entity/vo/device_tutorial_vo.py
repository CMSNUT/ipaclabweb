from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Device_tutorialModel(BaseModel):
    """
    仪器教程表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tutorial_id: Optional[int] = Field(default=None, description='教程id')
    tutorial_name: Optional[str] = Field(default=None, description='教程名称')
    device_id: Optional[int] = Field(default=None, description='仪器id')
    tutorial_content: Optional[str] = Field(default=None, description='教程内容')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='tutorial_name', message='教程名称不能为空')
    def get_tutorial_name(self):
        return self.tutorial_name

    @NotBlank(field_name='device_id', message='仪器id不能为空')
    def get_device_id(self):
        return self.device_id


    def validate_fields(self):
        self.get_tutorial_name()
        self.get_device_id()




class Device_tutorialQueryModel(Device_tutorialModel):
    """
    仪器教程不分页查询模型
    """
    pass


@as_query
class Device_tutorialPageQueryModel(Device_tutorialQueryModel):
    """
    仪器教程分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDevice_tutorialModel(BaseModel):
    """
    删除仪器教程模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    tutorial_ids: str = Field(description='需要删除的教程id')
