from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Instrument_tutorialModel(BaseModel):
    """
    仪器教程表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tutorial_id: Optional[int] = Field(default=None, description='教程ID')
    instrument_id: Optional[int] = Field(default=None, description='仪器ID')
    tutorial_title: Optional[str] = Field(default=None, description='教程标题')
    tutorial_category: Optional[str] = Field(default=None, description='教程类别')
    tutorial_file: Optional[str] = Field(default=None, description='本地文件')
    tutorial_url: Optional[str] = Field(default=None, description='外部链接')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='tutorial_title', message='教程标题不能为空')
    def get_tutorial_title(self):
        return self.tutorial_title


    def validate_fields(self):
        self.get_tutorial_title()




class Instrument_tutorialQueryModel(Instrument_tutorialModel):
    """
    仪器教程不分页查询模型
    """
    pass


@as_query
class Instrument_tutorialPageQueryModel(Instrument_tutorialQueryModel):
    """
    仪器教程分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteInstrument_tutorialModel(BaseModel):
    """
    删除仪器教程模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    tutorial_ids: str = Field(description='需要删除的教程ID')
