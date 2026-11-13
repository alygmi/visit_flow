from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str


class LoginResponse(BaseModel):
    token: str
    user: UserOut


class ActivityCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    entity_id: str = Field(alias="entityId", min_length=1)
    segment: str
    visit_date: str = Field(alias="visitDate", min_length=1)


class ActivityStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
