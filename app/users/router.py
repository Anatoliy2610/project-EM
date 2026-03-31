from typing import List

from fastapi import (APIRouter, Depends, Form, HTTPException, Request,
                     Response, status)
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session, selectinload

from app.config import (create_access_token, get_current_user, get_db,
                        get_password_hash, templates, verify_password)
from app.users.models import UserModel
from app.users.schemas import UpdateUser, User, UserAuth, UserCreate

router = APIRouter(tags=["Пользователь"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: UserModel = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request, name="base.html", context={"current_user": current_user}
    )


@router.get("/users", response_model=List[User])
async def get_users(
    request: Request,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    users_data = db.query(UserModel).options(selectinload(UserModel.team)).all()
    return templates.TemplateResponse(
        request=request,
        name="users/users.html",
        context={"users_data": users_data, "current_user": current_user},
    )


@router.get("/register-form/", response_class=HTMLResponse)
async def show_register_form(
    request: Request, current_user: UserModel = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "users/register.html", {"request": request, "current_user": current_user}
    )


@router.post("/register/")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )
    db_user = UserModel(
        email=user_data.email, hash_password=get_password_hash(user_data.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Вы успешно зарегистрированы!"}


@router.get("/login-form/", response_class=HTMLResponse)
async def show_login_form(
    request: Request, current_user: UserModel = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "users/login.html", {"request": request, "current_user": current_user}
    )


@router.post("/login/")
async def auth_user(
    user_data: UserAuth, response: Response, db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if user is None or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    access_token = create_access_token({"sub": str(user.id)})
    response = JSONResponse(
        content={"access_token": access_token, "refresh_token": None}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Защита от XSS
        samesite="lax",  # Защита от CSRF
    )
    return response


@router.post("/logout/")
async def logout_user(
    response: Response, current_user: UserModel = Depends(get_current_user)
):
    response.delete_cookie(key="access_token")
    return {"message": "Пользователь успешно вышел из системы"}


@router.get("/user", response_model=User)
async def get_user(
    request: Request,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user_data = (
        db.query(UserModel)
        .filter(UserModel.email == current_user.email)
        .options(selectinload(UserModel.team))
        .first()
    )
    return templates.TemplateResponse(
        request=request,
        name="users/user.html",
        context={"user_data": user_data, "current_user": current_user},
    )


@router.get("/update_user")
async def get_update_user(
    request: Request, current_user: UserModel = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "users/update_user.html", {"request": request, "current_user": current_user}
    )


@router.patch("/update_user")
async def update_user(
    data_user: UpdateUser,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    if data_user.email:
        user.email = data_user.email
    if data_user.password:
        user.hash_password = get_password_hash(data_user.password)
    db.commit()
    return {"message": "Пользователь успешно изменен"}


@router.delete("/delete_user")
async def delete_user(
    response: Response,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    db.delete(user)
    db.commit()
    response.delete_cookie(key="access_token")
    return {"message": "Пользователь успешно удален"}
