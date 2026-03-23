from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session


from app.teams.models import TeamModel
from app.teams.schemas import DeleteUserSChema, TeamSchema, UserTeamSchema
from app.teams.utils import add_team_db, add_user_to_team_db, check_absence_user, check_availability_team, check_user_absence_role, check_user_admin, check_user_to_team, update_data_user_db, update_user_to_team_db
from app.users.models import UserModel

from app.config import get_current_user, get_db
from app.users.schemas import User
from app.config import templates


router = APIRouter(tags=['Команда'])


@router.get("/teams", response_model=List[TeamSchema])
async def get_teams(request: Request, db: Session = Depends(get_db)):
    teams_data = db.query(TeamModel).all()
    return templates.TemplateResponse(
        request=request, name="teams/teams.html", context={"teams_data": teams_data}
    )


@router.post("/add_team")
async def add_teams(data_team: TeamSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "name": "string"
    }
    '''
    team = db.query(TeamModel).filter(TeamModel.name == data_team.name).first()
    check_availability_team(team=team)
    check_user_absence_role(role=user_data.role)
    add_team_db(data_team, db)
    update_data_user_db(data_user=user_data, data_team=data_team, db=db)
    return {'message': 'Команда зарегистрирована!'}


@router.patch('/user_to_team')
async def add_or_update_user_to_team(data_user: UserTeamSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "email_user": "string",
    "role": "string"
    }
    '''
    check_user_admin(user_data.role)
    user = db.query(UserModel).filter(UserModel.email == data_user.email_user).first()
    check_absence_user(user)
    if user.role:
        check_user_to_team(user_admin=user, user_data=user_data)
        update_user_to_team_db(user=user, new_role=data_user.role, db=db)
        return {'message': f'Пользователь {user.email} команды {user.team.name} получил новую роль {data_user.role}'}
    add_user_to_team_db(user=user, user_data=user_data, new_data_user=data_user, db=db)
    return {'message': f'Пользователь {user.email} добавлен в команду {user_data.team.name} с ролью {user.role}'}


@router.get("/team", response_model=List[User])
async def get_team(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    team = db.query(UserModel).filter(UserModel.team_id == user_data.team_id).all()
    return team


@router.patch('/delete_user_to_team')
async def delete_user_team(data_user: DeleteUserSChema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "email_user": "string"
    }
    '''
    check_user_admin(user_data.role)
    user = db.query(UserModel).filter(UserModel.email == data_user.email_user).first()
    check_absence_user(user)
    check_user_to_team(user_admin=user_data, user_data=user)
    user.role = None
    user.team_id = None
    db.commit()
    return {'message': f'Пользователь {data_user.email_user} удален из команды'}
