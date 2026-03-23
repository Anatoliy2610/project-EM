from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session, selectinload
from datetime import datetime

from app.calendar.schemas import CalendarSchemas
from app.meetings.models import MeetingModel
from app.tasks.models import TaskModel
from app.tasks.schemas import EvaluationSchema, JobResultSchema, TaskAddUpdateSchema, TaskDeleteSchema, TaskSchema
# from app.users.models import UserModel
from app.calendar.config import get_table_day, get_table_month
from app.config import get_current_user, get_db
from app.users.models import UserModel
from app.config import templates


router = APIRouter(tags=['Календарь'])



# @router.get("/tasks", response_model=List[TaskSchema])
@router.get("/calendar")
async def get_calendar(request: Request, dates: CalendarSchemas, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    result = []
    if dates.second_data:
        data_tasks = db.query(TaskModel).filter(
            TaskModel.executor_id == user_data.id, 
            TaskModel.dedline >= dates.first_data, 
            TaskModel.dedline <= dates.second_data).all()
        data_users = db.query(UserModel).filter(UserModel.id == user_data.id).first()
        data_meetings = data_users.meetings
        for data in data_meetings:
            res = {}
            if data.datetime_beginning <= dates.first_data and data.datetime_end:
                res['name'] = data.name
                res['date'] = data.datetime_beginning
                result.append(res)
        for data in data_tasks:
            res = {}
            res['name'] = data.name
            res['date'] = data.dedline
            result.append(res)
        sorted_meetings = sorted(result, key=lambda x: x['date'])
        print(sorted_meetings)
        table = get_table_month(sorted_meetings)
        print(table)
        return templates.TemplateResponse(
            request=request, name="calendar/calendar.html", context={"result": table}
        )
    data_tasks = db.query(TaskModel).filter(TaskModel.executor_id == 3, TaskModel.dedline == dates.first_data).order_by(TaskModel.dedline.desc()).all()
    data_users = db.query(UserModel).filter(UserModel.id == 3).first()
    data_meetings = data_users.meetings
    for data in data_meetings:
        res = {}
        if data.datetime_beginning == dates.first_data:
            res['name'] = data.name
            res['date'] = data.datetime_beginning
            result.append(res)
    for data in data_tasks:
        res = {}
        res['name'] = data.name
        res['date'] = data.dedline
        result.append(res)
    sorted_meetings = sorted(result, key=lambda x: x['date'])
    print(sorted_meetings)
    table = get_table_day(sorted_meetings)
    print(table)
    return templates.TemplateResponse(
        request=request, name="calendar/calendar.html", context={"result": table}
    )
