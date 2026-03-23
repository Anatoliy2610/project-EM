from fastapi import APIRouter, HTTPException, status, Depends, Response, Request, Form
from typing import List
from sqlalchemy.orm import Session, selectinload
from fastapi.responses import HTMLResponse


# from tel_bot.users.utils import (get_db, get_password_hash, verify_password, create_access_token, get_current_user)
# from tel_bot.users.models import UserModel, UserAuthModel, User
# from tel_bot.users.shemas import UserRegister
from app.teams.models import TeamModel
from app.users.models import UserModel
from app.users.schemas import User, UserCreate, UserRegister, UserAuth
from app.config import create_access_token, get_current_user, get_db, get_password_hash, verify_password
from app.config import templates

router = APIRouter(tags=['Пользователь'])



# ### 1. Пользователи
# - Регистрация с email и паролем
# - Авторизация / выход
# - Роли: обычный пользователь, менеджер, админ команды
# - Обновление профиля
# - Удаление аккаунта (без восстановления)
# - Привязка к команде по коду (опционально)




@router.get("/users", response_model=List[User])
async def get_users(request: Request, db: Session = Depends(get_db)):
    users_data = db.query(UserModel).options(
        selectinload(UserModel.team)
    ).all()
    return templates.TemplateResponse(
        request=request, name="users/users.html", context={"users_data": users_data}
    )


# нужно реализовать каждый эндпоинт по отдельности!!!!!!!!!!!!!!!!!!!!!!!!
# начинать с user - teams - tasks - meetings - и реализовать календарь



@router.get("/register-form/", response_class=HTMLResponse)
async def show_register_form(request: Request):
    print(request.method)
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    db_user = UserModel(
        email=user_data.email,
        hash_password = get_password_hash(user_data.password)
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.get("/login-form/", response_class=HTMLResponse)
async def show_login_form(request: Request):
    print(request.method)
    return templates.TemplateResponse("users/login.html", {"request": request})


@router.post("/login/")
async def auth_user(user_data: UserAuth, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if user is None or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль'
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {'access_token': access_token, 'refresh_token': None}



@router.get("/me/")
async def get_me(user_data: UserModel = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
