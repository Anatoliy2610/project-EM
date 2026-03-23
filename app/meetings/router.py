from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session, selectinload
from datetime import datetime, timedelta

from app.meetings.models import MeetingModel
from app.meetings.schemas import MeetinAddSchema, MeetingSchema, MeetingSchemaDelete
# from app.users.models import UserModel

from app.config import get_current_user, get_db
from app.meetings.utils import add_meeting_db, check_meeting, check_not_meeting, check_participants, check_user_admin, delete_meeting_db
from app.users.models import UserModel
from app.config import templates



'''
сделал пользователей, задачи и команды

нужно сделать встречи (вывести логику в utils.py)
переделать логику в календаре (добавить, чтобы данные выводились в json) - можно ещё сделать html шаблон с таблицей

нужно подключить админку
подключить линтеры и проверку импортов
(можно написать тесты)

попробовать сдать без визуальной части

'''




router = APIRouter(tags=['Встречи'])


@router.get("/meetings", response_model=List[MeetingSchema])
async def get_meetings(request: Request, db: Session = Depends(get_db)):
    meetings_data = db.query(MeetingModel).options(
        selectinload(MeetingModel.participants)
    ).all()
    return templates.TemplateResponse(
        request=request, name="meetings/meetings.html", context={"meetings_data": meetings_data}
    )


@router.post("/add_meeting")
async def add_meeting(data_meeting: MeetinAddSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    check_user_admin(user_role=user_data.role)
    meeting = db.query(MeetingModel).filter(
        MeetingModel.datetime_beginning <= data_meeting.datetime_beginning, data_meeting.datetime_beginning <= MeetingModel.datetime_end).first()
    check_meeting(meeting=meeting)
    participants = db.query(UserModel).filter(UserModel.id.in_(data_meeting.participants), UserModel.team_id == user_data.team_id).all()
    check_participants(participants=participants, user_data=user_data)
    add_meeting_db(data_meeting=data_meeting, user_data=user_data, participants=participants, db=db)
    return {"message": f"Назначена встреча в {data_meeting.datetime_beginning}"}


@router.delete('/delete_meeting')
async def delete_meeting(data_meeting: MeetingSchemaDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    check_user_admin(user_role=user_data.role)
    meeting = db.query(MeetingModel).filter(
        MeetingModel.datetime_beginning == data_meeting.datetime_beginning, 
        MeetingModel.name == data_meeting.name, 
        MeetingModel.team_id == user_data.team_id).first()
    check_not_meeting(meeting=meeting)
    delete_meeting_db(meeting=meeting, db=db)
    return {"message": f"Удалена встреча '{data_meeting.name}' начало в {data_meeting.datetime_beginning}"}


@router.get("/meetings_user", response_model=List[MeetingSchema])
async def get_meetings(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    meetings = db.query(UserModel).filter(UserModel.id == user_data.id).first()
    return meetings.meetings
