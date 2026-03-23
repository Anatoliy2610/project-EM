from pydantic import BaseModel


class TeamSchema(BaseModel):
    name: str


class UserTeam(BaseModel):
    email_user: str
    role: str = None
