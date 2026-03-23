from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    executor_id = Column(Integer, ForeignKey('users.id'))
    executor = relationship('UserModel')

    status = Column(String, default='открыто')
    dedline = Column(DateTime)
    description = Column(String, nullable=True)
    chat = Column(String, nullable=True) # нужно будет сделать таблицу под чат и совместить (многие ко многим)
    job_evaluation = Column(Integer, nullable=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('TeamModel')

    