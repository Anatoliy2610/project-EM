from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.main import app
from app.config import get_current_user, get_db
from app.database import Base
from app.meetings.models import MeetingModel
from app.tasks.models import TaskModel
from app.teams.models import TeamModel
from app.users.models import UserModel


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture(scope='session')
def get_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='session')
def create_db():
    Base.metadata.create_all(bind=engine)
    yield
    os.remove("test.db")


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
def get_fixture_db():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


def override_get_current_user():
    test_user = UserModel(
        id=1, 
        email='User1@mail.ru', 
        role=None, 
        team_id=None, 
        team=TeamModel(),
        tasks=[TaskModel()],
        meetings=[MeetingModel()]
        )
    return test_user


@pytest.fixture
def get_fixture_current_user():
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.clear()


def override_get_current_user_admin():
    test_user = UserModel(
        id=1, 
        email='User1@mail.ru', 
        role='админ команды', 
        team_id=1, 
        team=TeamModel(name='team1'),
        tasks=[TaskModel()],
        meetings=[MeetingModel()]
        )
    return test_user


@pytest.fixture
def get_fixture_current_user_admin():
    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    yield
    app.dependency_overrides.clear()

