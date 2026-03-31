import pytest
from app.users.models import UserModel
from tests.test_api.conftest import client

from app.main import app
from app.config import get_current_user



class TestUserClientAPI:

    def test_get_users(self, get_client):
        response = get_client.get('/users')
        assert response.status_code == 200

    def test_register_user(self, get_client, get_fixture_db):
        response = get_client.post('/register', json={
            "email": "User1@mail.ru",
            "password": "User1-password"
            })
        assert response.status_code == 200
        response = get_client.post('/register', json={
            "email": "User1@mail.ru",
            "password": "User1-password"
            })
        assert response.status_code == 409


    def test_auth_user(self, get_client, get_fixture_db):
        response = get_client.post('/login', json={
            "email": "User1@mail.ru",
            "password": "User1-password"
            })
        assert response.status_code == 200
        response = get_client.post('/login', json={
            "email": "ErrorEmail@mail.ru",
            "password": "Error-password"
            })
        assert response.status_code == 401

    def test_get_user(self, get_client, get_fixture_current_user, get_fixture_db):
        response = get_client.get('/user')
        assert response.status_code == 200


    def test_update_user(self, get_client, get_fixture_current_user, get_fixture_db):
        response = get_client.get('/update_user')
        assert response.status_code == 200
        response = client.patch('/update_user', json={'email': 'User1@mail.ru', 'password': 'password'})
        assert response.status_code == 200

    def test_delete_user(self, get_client, get_fixture_current_user, get_fixture_db):
        response = get_client.delete('/delete_user')
        assert response.status_code == 200
