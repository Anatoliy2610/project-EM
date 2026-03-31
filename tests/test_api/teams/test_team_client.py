import pytest

from tests.test_api.conftest import client




class TestTeamClientAPI:
    def test_get_teams(self, get_client, create_db, get_fixture_db, get_fixture_current_user):
        response = get_client.get("/teams")
        assert response.status_code == 200

    def test_get_add_team(self, get_client, get_fixture_db, get_fixture_current_user):
        response = get_client.get("/add_team")
        assert response.status_code == 200

    def test_add_teams(self, get_client, get_fixture_db, get_fixture_current_user):
        response = get_client.post("/add_team", json={"name": "team1"})
        assert response.status_code == 200
        response = get_client.post("/add_team", json={"name": "team1"})
        assert response.status_code == 409
  
  
    def test_get_add_or_update_user_to_team(self, get_client, get_fixture_db, get_fixture_current_user_admin):
        response = get_client.get("/user_to_team")
        assert response.status_code == 200

    def test_add_or_update_user_to_team(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        response = get_client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
        assert response.status_code == 200
        response = get_client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'менеджер'})
        assert response.status_code == 200
        response = get_client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'нет роли'})
        assert response.status_code == 409
        response = get_client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
        assert response.status_code == 200

    def test_get_team(self, get_client, get_fixture_db, get_fixture_current_user_admin):
        response = get_client.get('/team')
        assert response.status_code == 200

    def test_delete_user_team(self, get_client, get_fixture_db, get_fixture_current_user_admin):
        response = get_client.patch('/delete_user_to_team', json={'email_user': 'User2@mail.ru'})
        assert response.status_code == 200
        response = get_client.patch('/delete_user_to_team', json={'email_user': 'User2@mail.ru'})
        assert response.status_code == 409
