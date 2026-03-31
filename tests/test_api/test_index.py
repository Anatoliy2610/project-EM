import pytest
from app.users.models import UserModel
from tests.test_api.conftest import client

from app.main import app
from app.config import get_current_user



class TestUserAPI:

    def test_index(self, create_db):
        response = client.get("/")
        assert response.status_code == 200
    