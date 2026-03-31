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
    """
    Отображает ежемесячный календарь для текущего пользователя с его встречами и задачами.
    """

    today = date.today()
    year, month = today.year, today.month
    cal = calendar.monthcalendar(year, month)
    monthly_calendar_data: Dict[int, Dict[str, Any]] = {} 

    # Собираем все релевантные события и задачи пользователя
    user_events: List[Dict[str, Any]] = []
    # Встречи
    user_data = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    get_data_meeting(user_events=user_events, user_data=user_data)
    # for meeting in user_data.meetings:
    #     # Проверяем, является ли пользователь участником встречи
    #     is_participant = any(p.id == current_user.id for p in meeting.participants)
    #     if is_participant:
    #         user_events.append(
    #             {
    #                 "type": "meeting",
    #                 "id": meeting.id,
    #                 "title": meeting.name,
    #                 "start_time": meeting.datetime_beginning,
    #                 "end_time": meeting.datetime_end,
    #             }
    #         )
    # Задачи
    get_data_task(user_events=user_events, user_data=user_data)
    # for task in user_data.tasks:
    #     user_events.append(
    #         {
    #             "type": "task",
    #             "id": task.id,
    #             "title": task.name,
    #             "due_date": task.dedline,  # Используем 'dedline' из модели TaskModel
    #         }
    #     )

    # Структурируем события по дням
    get_monthly_calendar_data(monthly_calendar_data=monthly_calendar_data,
                              cal=cal, 
                              year=year, 
                              month=month, 
                              user_events=user_events)
    # for week in cal:
    #     for day_num in week:
    #         if day_num == 0:  # Пропускаем дни, не относящиеся к текущему месяцу
    #             continue

    #         current_day_date = date(year, month, day_num)
    #         # day_data: Dict[str, Any] = {"date": current_day_date, "items": []}
    #         day_details: Dict[str, Any] = {
    #             "date": current_day_date,
    #             "events_list": [],
    #         }  # Изменили 'items' на 'events_list'

    #         # Находим события и задачи для этого дня
    #         for event in user_events:
    #             if event["type"] == "meeting":
    #                 if event["start_time"].date() == current_day_date:
    #                     day_details["events_list"].append(event)
    #             elif event["type"] == "task":
    #                 # Для задач отображаем их в день дедлайна
    #                 if (
    #                     event["due_date"]
    #                     and event["due_date"].date() == current_day_date
    #                 ):
    #                     day_details["events_list"].append(event)

    #         # Сортируем элементы в дне по времени (встречи сначала, потом задачи)
    #         day_details["events_list"].sort(
    #             key=lambda x: (
    #                 0 if x["type"] == "meeting" else 1,  # Сначала встречи
    #                 x.get("start_time", datetime.max),  # По времени начала встречи
    #             )
    #         )

    #         monthly_calendar_data[current_day_date.isoformat()] = (
    #             day_details  # Используем ISO формат даты как ключ
    #         )
    # --- Подготовка данных для дневного вида (опционально, но полезно для ссылок) ---
    # Этот блок можно упростить, если дневной вид не нужен в шаблоне напрямую,
    # а генерируется по запросу. Но для ссылок из месячного вида он удобен.
    daily_calendar_data: Dict[str, Dict[int, List[Dict[str, Any]]]] = {}

    get_daily_calendar_data(monthly_calendar_data, daily_calendar_data=daily_calendar_data)

    # for day_key, day_info in monthly_calendar_data.items():
    #     date_obj = date.fromisoformat(day_key)
    #     hours_data: Dict[int, List[Dict[str, Any]]] = {}

    #     for item in day_info["events_list"]:
    #         hour = -1  # Для задач без конкретного времени
    #         if item["type"] == "meeting":
    #             hour = item["start_time"].hour
    #         # Если задача имеет конкретное время (можно добавить поле в TaskModel),
    #         # можно использовать его. Иначе, задачи можно группировать отдельно.
    #         # Пока оставим задачи с hour = -1 для общей группы "без времени".

    #         if hour not in hours_data:
    #             hours_data[hour] = []
    #         hours_data[hour].append(item)

    #     # Сортируем элементы внутри каждого часа (или группы -1)
    #     for h in hours_data:
    #         hours_data[h].sort(key=lambda x: x.get("start_time", datetime.max))

    #     daily_calendar_data[day_key] = hours_data
    # Передаем данные в шаблон
    context = {
        "request": request,
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "calendar_grid": cal,  # Структура для построения сетки календаря
        "monthly_events": monthly_calendar_data,  # События, сгруппированные по дням
        "daily_schedule": daily_calendar_data,  # Детальное расписание по часам
        "current_user": current_user,
        "date": date,
    }
    return templates.TemplateResponse("calendar/calendar.html", context)
