import pytest


class TestMeetingAPI:
    def test_get_meetings(self, get_client, create_db, get_fixture_db, get_fixture_current_user_admin):
        response = get_client.get("/meetings")
        assert response.status_code == 200


    def test_get_add_meeting(self, get_client, get_fixture_db, get_fixture_current_user_admin):
        response = get_client.get("/add_meeting")
        assert response.status_code == 200

    def test_add_meeting(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        response = get_client.patch("/user_to_team", json={'email_user': 'UserMeeting1@mail.ru', 'role': 'сотрудник'})
        assert response.status_code == 200
        response = get_client.patch("/user_to_team", json={'email_user': 'UserMeeting2@mail.ru', 'role': 'менеджер'})
        assert response.status_code == 200
        response = get_client.post("/add_meeting", json={
            'name': 'name meeting',
            'datetime_beginning': '2025-03-31',
            'participants': [1, 2]
        })
        assert response.status_code == 200
        response = get_client.post("/add_meeting", json={
            'name': 'name meeting',
            'datetime_beginning': '2025-03-31',
            'participants': [1, 25, 30]
        })
        assert response.status_code == 409

    def test_get_meetings_user(self, get_client, create_db, get_fixture_db, get_fixture_current_user):
        response = get_client.get("/meetings_user/1")
        assert response.status_code == 200
