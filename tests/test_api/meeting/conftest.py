import pytest

from tests.test_api.conftest import client

@pytest.fixture
def add_data_for_db():   
    new_user2 = client.post('/register', json={
            "email": "UserMeeting1@mail.ru",
            "password": "User2-password"
            })
    new_user3 = client.post('/register', json={
            "email": "UserMeeting2@mail.ru",
            "password": "User3-password"
            })
