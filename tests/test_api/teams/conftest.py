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
from tests.test_api.conftest import client


@pytest.fixture
def add_data_for_db():
    new_user2 = client.post('/register', json={
            "email": "User2@mail.ru",
            "password": "User2-password"
            })
    new_user3 = client.post('/register', json={
            "email": "User3@mail.ru",
            "password": "User3-password"
            })
