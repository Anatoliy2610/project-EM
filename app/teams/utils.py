from fastapi import HTTPException, status

from app.teams.models import TeamModel



def check_availability_team(team):
    if team:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Команда с таким названием уже существует'
        )
    

def check_user_absence_role(role):
    if role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы уже состоите в команде'
        )


def check_user_admin(user_role):
    if user_role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У Вас не достаточно прав'
        )
    
    
def check_absence_user(user):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователя не существует'
        )


def add_team_db(data_team, db):
    db_team = TeamModel(
        name=data_team.name
        )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)


def update_data_user_db(data_user, data_team, db):
    new_team_id = db.query(TeamModel).filter(TeamModel.name == data_team.name).first()
    data_user.team_id = new_team_id.id
    data_user.role = 'админ команды'
    db.commit()


def check_role(role):
    if role not in ('менеджер', 'сотрудник'):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='такой роли не существует'
        )


def add_user_to_team_db(user, user_data, new_data_user, db):
    check_role(new_data_user.role)
    user.role = new_data_user.role
    user.team = user_data.team
    db.commit()


def update_user_to_team_db(user, new_role, db):
    check_role(new_role)
    user.role = new_role
    db.commit()


def check_user_to_team(user_admin, user_data):
    if user_admin.team_id != user_data.team_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь не состоит в вашей команде'
        )
