from pydantic import BaseModel

from typing import List

from app.teams.schemas import TeamSchema
from app.users.schemas import User
from datetime import datetime


class MeetingSchema(BaseModel):
    name: str
    datetime_beginning: datetime
    datetime_end: datetime
    team_id: int | None#None временно
    team: TeamSchema
    participants: List[User]


class MeetinAddSchema(BaseModel):
    name: str
    datetime_beginning: datetime
    participants: List[int]


class MeetingSchemaDelete(BaseModel):
    name: str
    datetime_beginning: datetime


class MeetingsUserSchema(BaseModel):
    name: str
    datetime_beginning: datetime
    datetime_end: datetime
    team_id: int | None#None временно
    team: TeamSchema
    participants: List[User]
