from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class DeviceModel(BaseModel):
    """
    仪器管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    device_id: Optional[int] = Field(default=None, description='仪器id')
    device_name: Optional[str] = Field(default=None, description='仪器名称')
    device_img: Optional[str] = Field(default=None, description='仪器图片地址')
    device_desc: Optional[str] = Field(default=None, description='仪器简介')
    create_by: Optional[str] = Field(default=None, description='创建人')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新人')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='device_name', message='仪器名称不能为空')
    def get_device_name(self):
        return self.device_name


    def validate_fields(self):
        self.get_device_name()




class DeviceQueryModel(DeviceModel):
    """
    仪器管理不分页查询模型
    """
    pass


@as_query
class DevicePageQueryModel(DeviceQueryModel):
    """
    仪器管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDeviceModel(BaseModel):
    """
    删除仪器管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    device_ids: str = Field(description='需要删除的仪器id')
