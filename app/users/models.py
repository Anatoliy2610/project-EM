from pydantic import EmailStr
from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

# from fastapi_users.models import M

from app.database import Base
from app.meetings.models import meeting_participants



class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    role = Column(String, nullable=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)
    team = relationship('TeamModel')

    hash_password = Column(String)

    meetings = relationship('MeetingModel', secondary=meeting_participants, back_populates='participants')



