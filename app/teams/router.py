from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session


from app.teams.models import TeamModel
from app.teams.schemas import TeamSchema, UserTeam
from app.users.models import UserModel

from app.config import get_current_user, get_db
from app.users.schemas import User
from app.config import templates


router = APIRouter(tags=['Команда'])



# ### 2. Команды
# - Админ создаёт компанию / команду
# - Добавление/удаление пользователей в команде
# - Просмотр состава команды
# - Назначение ролей (менеджер, сотрудник)

@router.get("/teams", response_model=List[TeamSchema])
async def get_teams(request: Request, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    teams_data = db.query(TeamModel).all()
    return templates.TemplateResponse(
        request=request, name="teams/teams.html", context={"teams_data": teams_data}
    )


@router.post("/add_team")
async def add_teams(data_team: TeamSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    team = db.query(TeamModel).filter(TeamModel.name == data_team.name).first()
    if team:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Команда с таким названием уже существует'
        )
    if user_data.role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Вы уже состоите в команде'
        )
    user_data.role = 'админ команды'
    db_team = TeamModel(
        name=data_team.name
        )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return {'message': 'Команда зарегистрирована!'}


@router.patch('/user_to_team')
async def add_or_update_user_to_team(data_user: UserTeam, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    user = db.query(UserModel).filter(UserModel.email == data_user.email_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователя не существует'
        )
    if user.role:
        if user.team_id == user_data.team_id:
            user.role_team = user_data.role
            db.commit()
            return {'message': f'Пользователь {user.email} команды {user.team.name} получил новую роль {data_user.role}'}
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь состоит в другой команде'
        )
    user.role = data_user.role
    user.team_id = user.team_id
    db.commit()
    return {'message': f'Пользователь {user.email} добавлен в команду {user.team.name} с ролью {user.role}'}


@router.get("/team", response_model=List[User])
async def get_team(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    team = db.query(UserModel).filter(UserModel.team_id == user_data.team_id).all()
    return team


@router.patch('/delete_user_to_team')
async def delete_user_team(data_user: UserTeam, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно полномочий'
        )

    user = db.query(UserModel).filter(UserModel.email == data_user.email_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователя не существует'
        )
    if user_data.team_id != user.team_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь не состоит в вашей команде'
        )
    user.role_team = None
    user.team_id = None
    db.commit()
    return {'message': f'Пользователь {data_user.email_user} удален из команды'}



