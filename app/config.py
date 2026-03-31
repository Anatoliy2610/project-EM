import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.users.models import UserModel

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv()
SECRET_KEY_TOKEN = os.getenv("SECRET_KEY_TOKEN")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if (
        not user
        or verify_password(plain_password=password, hashed_password=user.hash_password)
        is False
    ):
        return None
    return user


def get_auth_data():
    return {"secret_key": SECRET_KEY_TOKEN, "algorithm": ALGORITHM}


async def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> UserModel:
    """
    Извлекает и валидирует текущего пользователя из cookie-файла "access_token".
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    try:
        auth_config = get_auth_data()
        payload = jwt.decode(
            access_token,
            auth_config["secret_key"],
            algorithms=[auth_config["algorithm"]],
        )
        expire_timestamp = payload.get("exp")
        if expire_timestamp is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен (нет exp)",
            )
        expire_time = datetime.fromtimestamp(int(expire_timestamp), tz=timezone.utc)
        # Проверяем, не истек ли срок действия токена
        if expire_time < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истек",
            )
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен (нет sub)",
            )
        user = db.query(UserModel).filter(UserModel.id == int(user_id_str)).first()
        if user is None:
            return None
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка при проверке токена",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат ID пользователя в токене",
        )
    except Exception as e:
        print(f"Неожиданная ошибка в get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при аутентификации",
        )


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
