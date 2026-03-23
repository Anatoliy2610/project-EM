from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session, selectinload
from datetime import datetime, timedelta

from app.meetings.models import MeetingModel
from app.meetings.schemas import MeetinAddSchema, MeetingSchema, MeetingSchemaDelete
# from app.users.models import UserModel

from app.config import get_current_user, get_db
from app.users.models import UserModel
from app.config import templates


router = APIRouter(tags=['Встречи'])


# ### 5. Встречи
# - Назначение встречи: дата, время, участники
# - Проверка времени (чтобы не накладывались события)
# - Список встреч пользователя
# - Возможность отменить встречу

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
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    meeting = db.query(MeetingModel).filter(
        MeetingModel.datetime_beginning <= data_meeting.datetime_beginning, data_meeting.datetime_beginning <= MeetingModel.datetime_end).first()
    if meeting:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='На это время уже запланирована встреча'
        )
    check_users = db.query(UserModel).filter(UserModel.id.in_(data_meeting.participants), UserModel.team_id == user_data.team_id).all()
    if len(data_meeting.participants) !=  len(check_users):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Есть участники, которые не состоят в вашей команде'
        )
    db_meeting = MeetingModel(
        name = data_meeting.name,
        datetime_beginning = data_meeting.datetime_beginning,
        datetime_end = data_meeting.datetime_beginning + timedelta(hours=1),
        team_id = user_data.team_id
    )
    db_meeting.participants = check_users
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return {"message": f"Назначена встреча в {data_meeting.datetime_beginning}"}


@router.delete('/delete_meeting')
async def delete_meeting(data_meeting: MeetingSchemaDelete, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    meeting = db.query(MeetingModel).filter(
        MeetingModel.datetime_beginning == data_meeting.datetime_beginning, 
        MeetingModel.name == data_meeting.name, 
        MeetingModel.team_id == user_data.team_id).first()

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Указанная встреча не найдена'
        )
    db.delete(meeting)
    db.commit()
    return {"message": f"Удалена встреча '{data_meeting.name}' начало в {data_meeting.datetime_beginning}"}


@router.get("/meetings_user", response_model=List[MeetingSchema])
async def get_meetings(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    meetings = db.query(UserModel).filter(UserModel.id == user_data.id).first()
    return meetings.meetings
