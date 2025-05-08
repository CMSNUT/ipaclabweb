from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class InstrumentModel(BaseModel):
    """
    仪器信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    instrument_id: Optional[int] = Field(default=None, description='仪器ID')
    instrument_name: Optional[str] = Field(default=None, description='仪器名称')
    instrument_model: Optional[str] = Field(default=None, description='仪器型号')
    instrument_remark: Optional[str] = Field(default=None, description='功能简介')
    instrument_room: Optional[str] = Field(default=None, description='存放位置')
    instrument_img: Optional[str] = Field(default=None, description='图片地址')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='instrument_name', message='仪器名称不能为空')
    def get_instrument_name(self):
        return self.instrument_name


    def validate_fields(self):
        self.get_instrument_name()




class InstrumentQueryModel(InstrumentModel):
    """
    仪器信息不分页查询模型
    """
    pass


@as_query
class InstrumentPageQueryModel(InstrumentQueryModel):
    """
    仪器信息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteInstrumentModel(BaseModel):
    """
    删除仪器信息模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    instrument_ids: str = Field(description='需要删除的仪器ID')
