from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from app.teams.schemas import TeamSchema


class User(BaseModel):
    email: str
    role: str | None
    role_team: str | None
    team_id: int  | None
    team: TeamSchema | None
    hash_password: str


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    email: str
    password: str = Field(...)

class UserAuth(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

