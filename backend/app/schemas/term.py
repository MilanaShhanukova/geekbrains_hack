from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

config = ConfigDict(from_attributes=True)


class TermSchema(BaseModel):
    name: str = Field(
        title="",
        description="",
    )
    description: str = Field(
        title="",
        description="",
    )

    # class Config:
    #     from_attributes = True
    #     json_schema_extra = {
    #         "example": {
    #             "name": "Name for Some term",
    #             "description": "Some term Description",
    #         }
    #     }


class TermResponse(BaseModel):
    model_config = config
    id: UUID = Field(
        title="Id",
        description="",
    )
    name: str = Field(
        title="",
        description="",
    )
    description: str = Field(
        title="",
        description="",
    )

    # class Config:
    #     from_attributes = True
    #     json_schema_extra = {
    #         "example": {
    #             "config_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #             "name": "Name for Some term",
    #             "description": "Some term Description",
    #         }
    #     }
