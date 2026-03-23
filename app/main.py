from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from sqladmin import Admin

from app.database import Base, engine
from app.users.router import router as user_router
from app.teams.router import router as team_router
from app.tasks.router import router as task_router
from app.meetings.router import router as meeting_router
from app.data_db.router import router as data
from app.calendar.router import router as calendar
from app.admin.admin_views import UserAdmin, TaskAdmin, TeamAdmin, MeetingAdmin


Base.metadata.create_all(bind=engine)


app = FastAPI()


admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
admin.add_view(TeamAdmin)
admin.add_view(MeetingAdmin)



app.include_router(data)


app.include_router(user_router)
app.include_router(team_router)
app.include_router(task_router)
app.include_router(meeting_router)
app.include_router(calendar)

