from app.database import SessionLocal
from passlib.context import CryptContext
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException, status, Depends
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates


from app.users.models import UserModel


templates = Jinja2Templates(directory='app/templates')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

load_dotenv()
SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or verify_password(plain_password=password, hashed_password=user.hash_password) is False:
        return None
    return user


def get_auth_data():
    return {"secret_key": SECRET_KEY_TOKEN, "algorithm": ALGORITHM}


# async def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
#     print(authorization)
#     if not authorization:
#         raise HTTPException(status_code=401, detail='не авторизован')
#     try:
#         auth_data = get_auth_data()
#         token_type, access_token = authorization.split()
#         payload = jwt.decode(access_token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
#     except ValueError:
#         raise HTTPException(status_code=401, detail='неправильный заголовок')
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
#     if token_type != 'Bearer':
#         raise HTTPException(status_code=401, detail='неправильный тип')
#     expire = payload.get('exp')
#     expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
#     if (not expire) or (expire_time < datetime.now(timezone.utc)):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
#     user_id = payload.get('sub')
#     if not user_id:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
#     user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
#     return user

async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> UserModel: # Указываем возвращаемый тип
    """
    Извлекает и валидирует текущего пользователя из заголовка Authorization.
    """
    print(f"Получен заголовок Authorization: {authorization}") # Логирование для отл
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Авторизация не предоставлена'
        )
    try:
        token_parts = authorization.split()
        if len(token_parts) != 2:
            raise ValueError('Некорректный формат токена (ожидается "Bearer <token>")')

        token_type, access_token = token_parts
        auth_config = get_auth_data() # Получаем конфигурацию один раз
        if token_type.lower() != 'bearer': # Регистронезависимая проверка
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверный тип токена (ожидается "Bearer")'
            )
        # Декодируем токен
        payload = jwt.decode(access_token, auth_config['secret_key'], algorithms=[auth_config['algorithm']])
        # Проверяем наличие и валидность срока годности
        expire_timestamp = payload.get('exp')
        if expire_timestamp is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Токен не содержит информации о сроке годности (exp)'
            )
        # Преобразуем timestamp в datetime с учетом UTC
        expire_time = datetime.fromtimestamp(int(expire_timestamp), tz=timezone.utc)
        if expire_time < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Срок действия токена истек'
            )
        # Получаем ID пользователя из токена
        user_id_str = payload.get('sub')
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='В токене отсутствует идентификатор пользователя (sub)'
            )

        # Получаем пользователя из базы данных
        try:
            user_id = int(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Некорректный формат ID пользователя в токене' # ID должен быть числом
            )
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Пользователь с указанным ID не найден'
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не является валидным JWT'
        )
    except ValueError as ve: # Ловим ValueError отдельно для сообщения о формате заголовка
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ve) # Используем сообщение об ошибке из split
        )
    except Exception as e:
        # Общий обработчик для непредвиденных ошибок
        print(f"Непредвиденная ошибка в get_current_user: {e}") # Логирование
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Внутренняя ошибка сервера при аутентификации'
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


