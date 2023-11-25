from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

config = ConfigDict(from_attributes=True)


class JobSchema(BaseModel):
    model_config = config
    status: str = Field(
        title="",
        description="",
    )
    date_started: str = Field(
        title="",
        description="",
    )

    # class Config:
    #     from_attributes = True
    #     json_schema_extra = {
    #         "example": {
    #             "name": "Name for Some Nonsense",
    #             "description": "Some Nonsense Description",
    #         }
    #     }


class JobResponse(BaseModel):
    model_config = config
    id: UUID = Field(
        title="Id",
        description="",
    )
    status: str = Field(
        title="",
        description="",
    )

class JobResultResponse(BaseModel):
    model_config = config
    id: UUID = Field(
        title="Id",
        description="",
    )
    status: str = Field(
        title="",
        description="",
    )
    result: list[dict] = Field(
        title="",
        description="",
    )


    # class Config:
    #     from_attributes = True
    #     json_schema_extra = {
    #         "example": {
    #             "config_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #             "name": "Name for Some Nonsense",
    #             "description": "Some Nonsense Description",
    #         }
    #     }
