from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from app.database import Base, engine
from app.users.router import router as user_router
from app.teams.router import router as team_router
from app.tasks.router import router as task_router
from app.meetings.router import router as meeting_router
from app.data_db.router import router as data
from app.calendar.router import router as calendar


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(data)


app.include_router(user_router)
app.include_router(team_router)
app.include_router(task_router)
app.include_router(meeting_router)
app.include_router(calendar)

