#__________________________________________________________________________________________#
#_____________________________добавление в бд данные_______________________________________#
from app.users.models import UserModel
from app.teams.models import TeamModel
from app.tasks.models import TaskModel
from app.meetings.models import MeetingModel
from app.config import get_db, get_password_hash


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime


router = APIRouter(tags=['добавление данных'])



data_teams = [
    {'name': 'name_team_1'},
    {'name': 'name_team_2'},
    {'name': 'name_team_3'},
    {'name': 'name_team_4'},
    {'name': 'name_team_5'},
]

data_users = [
        {'email': 'user1@mail.ru', 'role': 'админ команды', 'role_team': 'менеджер', 'team_id': 1, 'password': 'password_user1'},
        {'email': 'user2@mail.ru', 'role': 'менеджер', 'role_team': 'менеджер', 'team_id': 1, 'password': 'password_user2'},
        {'email': 'user3@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 1, 'password': 'password_user3'},
        {'email': 'user4@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 1, 'password': 'password_user4'},
        {'email': 'user5@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 1, 'password': 'password_user5'},
        {'email': 'user6@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 1, 'password': 'password_user6'},

        {'email': 'user7@mail.ru', 'role': 'админ команды', 'role_team': 'менеджер', 'team_id': 2, 'password': 'password_user7'},
        {'email': 'user8@mail.ru', 'role': 'менеджер', 'role_team': 'менеджер', 'team_id': 2, 'password': 'password_user8'},
        {'email': 'user9@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 2, 'password': 'password_user9'},
        {'email': 'user10@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 2, 'password': 'password_user10'},
        {'email': 'user11@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 2, 'password': 'password_user11'},
        {'email': 'user12@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 2, 'password': 'password_user12'},

        {'email': 'user13@mail.ru', 'role': 'админ команды', 'role_team': 'менеджер', 'team_id': 3, 'password': 'password_user13'},
        {'email': 'user14@mail.ru', 'role': 'менеджер', 'role_team': 'менеджер', 'team_id': 3, 'password': 'password_user14'},
        {'email': 'user15@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 3, 'password': 'password_user15'},
        {'email': 'user16@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 3, 'password': 'password_user16'},
        {'email': 'user17@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 3, 'password': 'password_user17'},
        {'email': 'user18@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 3, 'password': 'password_user18'},

        {'email': 'user19@mail.ru', 'role': 'админ команды', 'role_team': 'менеджер', 'team_id': 4, 'password': 'password_user19'},
        {'email': 'user20@mail.ru', 'role': 'менеджер', 'role_team': 'менеджер', 'team_id': 4, 'password': 'password_user20'},
        {'email': 'user21@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 4, 'password': 'password_user21'},
        {'email': 'user22@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 4, 'password': 'password_user22'},
        {'email': 'user23@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 4, 'password': 'password_user23'},
        {'email': 'user24@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 4, 'password': 'password_user24'},
        {'email': 'user25@mail.ru', 'role': 'пользователь', 'role_team': 'менеджсотрудникер', 'team_id': 4, 'password': 'password_user25'},

        {'email': 'user26@mail.ru', 'role': 'админ команды', 'role_team': 'менеджер', 'team_id': 5, 'password': 'password_user26'},
        {'email': 'user27@mail.ru', 'role': 'менеджер', 'role_team': 'менеджер', 'team_id': 5, 'password': 'password_user27'},
        {'email': 'user28@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 5, 'password': 'password_user28'},
        {'email': 'user29@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 5, 'password': 'password_user29'},
        {'email': 'user30@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 5, 'password': 'password_user30'},
        {'email': 'user31@mail.ru', 'role': 'пользователь', 'role_team': 'сотрудник', 'team_id': 5, 'password': 'password_user31'},
]

data_tasks = [
    {'name': 'name_task', 'executor_id': 2, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 3, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 4, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 5, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 4, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 7, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 8, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'name_task', 'executor_id': 9, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 2},
    {'name': 'name_task', 'executor_id': 10, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 2},
    {'name': 'name_task', 'executor_id': 11, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 2},
    {'name': 'name_task', 'executor_id': 12, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 2},
    {'name': 'name_task', 'executor_id': 11, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 2},
    {'name': 'name_task', 'executor_id': 11, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 2},
    {'name': 'name_task', 'executor_id': 14, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 3},
    {'name': 'name_task', 'executor_id': 15, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 3},
    {'name': 'name_task', 'executor_id': 16, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 3},
    {'name': 'name_task', 'executor_id': 17, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 3},
    {'name': 'name_task', 'executor_id': 18, 'dedline': '2026-03-20', 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 3},
]

data_meetings = [
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 20), 'datetime_end': datetime(2026, 3, 21), 'team_id': 1,'participants': [1, 2, 3, 4, 5, 6]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 22), 'datetime_end': datetime(2026, 3, 23), 'team_id': 1,'participants': [1, 2, 3, 4, 5, 6]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 24), 'datetime_end': datetime(2026, 3, 25), 'team_id': 1,'participants': [1, 2, 3, 4, 5, 6]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 26), 'datetime_end': datetime(2026, 3, 27), 'team_id': 1,'participants': [1, 2, 3, 4, 5, 6]},

    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 20), 'datetime_end': datetime(2026, 3, 21), 'team_id': 2,'participants': [7, 8, 9, 10, 11, 12]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 22), 'datetime_end': datetime(2026, 3, 23), 'team_id': 2,'participants': [7, 8, 9, 10, 11, 12]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 24), 'datetime_end': datetime(2026, 3, 25), 'team_id': 2,'participants': [7, 8, 9, 10, 11, 12]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 26), 'datetime_end': datetime(2026, 3, 27), 'team_id': 2,'participants': [7, 8, 9, 10, 11, 12]},

    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 20), 'datetime_end': datetime(2026, 3, 21), 'team_id': 3,'participants': [13, 14, 15, 16, 17, 18]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 22), 'datetime_end': datetime(2026, 3, 23), 'team_id': 3,'participants': [13, 14, 15, 16, 17, 18]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 24), 'datetime_end': datetime(2026, 3, 25), 'team_id': 3,'participants': [13, 14, 15, 16, 17, 18]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 26), 'datetime_end': datetime(2026, 3, 27), 'team_id': 3,'participants': [13, 14, 15, 16, 17, 18]},
    {'name': 'name_meeting_', 'datetime_beginning': datetime(2026, 3, 28), 'datetime_end': datetime(2026, 3, 29), 'team_id': 3,'participants': [13, 14, 15, 16, 17, 18]},

]



@router.post('/add_data')
async def add_data(db: Session = Depends(get_db)):
    for item in data_teams:
        db_teams = TeamModel(
            name = item.get('name')
        )
        db.add(db_teams)
        db.commit()
        db.refresh(db_teams)
    for item in data_users:
        db_users = UserModel(
            email = item.get('email'),
            role = item.get('role'),
            role_team = item.get('role_team'),
            team_id = item.get('team_id'),
            hash_password = get_password_hash(item.get('password')),
        )
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
    index = 0
    for item in data_tasks:
        index += 1
        db_tasks = TaskModel(
            name = item.get("name") + str(index),
            executor_id = item.get('executor_id'),
            dedline = datetime(2026, 3, 20),
            description = item.get("description") + str(index),
            chat = item.get("chat"),
            job_evaluation = item.get("job_evaluation"),
            team_id = item.get("team_id"),
        )
        db.add(db_tasks)
        db.commit()
        db.refresh(db_tasks)
    index = 0
    for item in data_meetings:
        index += 1
        db_meetings = MeetingModel(
            name = item.get("name") + str(index),
            datetime_beginning = item.get('datetime_beginning'),
            datetime_end = item.get('datetime_end'),
            team_id = item.get('team_id'),
        )
        # users = db.query(UserModel).filter(UserModel.id == db_meetings.team_id).all()
        users = db.query(UserModel).filter(UserModel.id.in_(item.get("participants"))).all()

        # db_meeting.participants = db.query(UserModel).filter(UserModel.id.in_(data_meeting.participants)).all()
        db_meetings.participants = users
        
        db.add(db_meetings)
        db.commit()
        db.refresh(db_meetings)

    return {'message': 'добавлены данные'}

#__________________________________________________________________________________________#
#__________________________________________________________________________________________#
data_tasks2 = [
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 23), 'description': 'description_new_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 24), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 25), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 21), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 26), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 19), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 27), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},
    {'name': 'new_name_task', 'executor_id': 3, 'dedline': datetime(2026, 3, 28), 'description': 'description_task', 'chat': '', 'job_evaluation': 0, 'team_id': 1},

    ]
data_meetings2 = [
    {'name': 'new_name_meeting_', 'datetime_beginning': datetime(2026, 4, 8), 'datetime_end': datetime(2026, 4, 9), 'team_id': 1,'participants': [1, 2, 3]},
    {'name': 'new_name_meeting_', 'datetime_beginning': datetime(2026, 4, 5), 'datetime_end': datetime(2026, 4, 6), 'team_id': 1,'participants': [1, 2, 3]},
    {'name': 'new_name_meeting_', 'datetime_beginning': datetime(2026, 4, 1), 'datetime_end': datetime(2026, 4, 2), 'team_id': 1,'participants': [1, 2, 3]},
    {'name': 'new_name_meeting_', 'datetime_beginning': datetime(2026, 4, 12), 'datetime_end': datetime(2026, 4, 13), 'team_id': 1,'participants': [1, 2, 3]},
]
@router.post('/add_data2')
async def add_data2(db: Session = Depends(get_db)):
    index = 0
    for item in data_tasks2:
        index += 1
        db_tasks = TaskModel(
            name = item.get("name") + str(index),
            executor_id = item.get('executor_id'),
            dedline = item.get("dedline"),
            description = item.get("description") + str(index),
            chat = item.get("chat"),
            job_evaluation = item.get("job_evaluation"),
            team_id = item.get("team_id"),
        )
        db.add(db_tasks)
        db.commit()
        db.refresh(db_tasks)


    index = 0
    for item in data_meetings2:
        index += 1
        db_meetings = MeetingModel(
            name = item.get("name") + str(index),
            datetime_beginning = item.get('datetime_beginning'),
            datetime_end = item.get('datetime_end'),
            team_id = item.get('team_id'),
        )
        users = db.query(UserModel).filter(UserModel.id.in_(item.get("participants"))).all()
        db_meetings.participants = users
        db.add(db_meetings)
        db.commit()
        db.refresh(db_meetings)
    return {'message': 'добавлены данные'}



from fastapi.responses import HTMLResponse
from fastapi import Request
from app.config import templates
# from fastapi.templating import Jinja2Templates


# templates = Jinja2Templates(directory='app/templates')

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )



