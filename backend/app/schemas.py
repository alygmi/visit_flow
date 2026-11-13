from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Segment = Literal["B2G", "B2B"]
ActivityStatus = Literal["VISITED", "NOT_VISITED"]


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
    segment: Segment
    visit_date: date = Field(alias="visitDate")


class ActivityStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ActivityStatus


class ActivityItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    entity_id: str | None = Field(alias="entityId")
    entity_name: str = Field(alias="entityName")
    entity_type: str = Field(alias="entityType")
    segment: str
    region: str
    visit_date: date = Field(alias="visitDate")
    status: str
    sales_id: int = Field(alias="salesId")
    sales_name: str = Field(alias="salesName")
    can_edit: bool = Field(alias="canEdit")


class ActivitySummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total: int
    visited: int
    not_visited: int = Field(alias="notVisited")


class ActivityListResponse(BaseModel):
    items: list[ActivityItem]
    summary: ActivitySummary


class EntityOption(BaseModel):
    id: str
    name: str
    type: str
    segment: str
    region: str
    label: str


class EntityListResponse(BaseModel):
    items: list[EntityOption]
