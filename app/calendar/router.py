import calendar
from datetime import date, datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.calendar.utils import get_daily_calendar_data, get_data_meeting, get_data_task, get_monthly_calendar_data
from app.config import get_current_user, get_db, templates
from app.users.models import UserModel

router = APIRouter(tags=["Календарь"])


@router.get("/user_calendar", response_class=HTMLResponse)
async def get_user_calendar(
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):

    today = date.today()
    year, month = today.year, today.month
    cal = calendar.monthcalendar(year, month)
    monthly_calendar_data: Dict[int, Dict[str, Any]] = {} 

    user_events: List[Dict[str, Any]] = []
    user_data = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    get_data_meeting(user_events=user_events, user_data=user_data)
    get_data_task(user_events=user_events, user_data=user_data)
    get_monthly_calendar_data(monthly_calendar_data=monthly_calendar_data,
                              cal=cal, 
                              year=year, 
                              month=month, 
                              user_events=user_events)

    daily_calendar_data: Dict[str, Dict[int, List[Dict[str, Any]]]] = {}
    get_daily_calendar_data(monthly_calendar_data, daily_calendar_data=daily_calendar_data)
    context = {
        "request": request,
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "calendar_grid": cal,
        "monthly_events": monthly_calendar_data,
        "daily_schedule": daily_calendar_data,
        "current_user": current_user,
        "date": date,
    }
    return templates.TemplateResponse("calendar/calendar.html", context)
