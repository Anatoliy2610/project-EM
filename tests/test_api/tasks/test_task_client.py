import pytest

from tests.test_api.conftest import client




class TestTaskAPI:
    def test_get_tasks(self, get_client, create_db, get_fixture_db, get_fixture_current_user):
        response = get_client.get("/tasks")
        assert response.status_code == 200

    def test_get_add_task(self, get_client, get_fixture_db, get_fixture_current_user):
        response = get_client.get("/add_task")
        assert response.status_code == 200

    def test_add_task(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
        assert add_user_to_team.status_code == 200
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'сотрудник'})
        assert add_user_to_team.status_code == 200
        response = get_client.post("/add_task", json={
            'name': 'task_1',
            'executor_id': 1,
            'dedline': '2026-04-15',
            'description': 'Описание задачи'
        })
        assert response.status_code == 200
        response = get_client.post("/add_task", json={
            'name': 'task_1',
            'executor_id': 10,
            'dedline': '2026-04-15',
            'description': 'Описание задачи'
        })
        assert response.status_code == 404


    def test_add_message_chat(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
        add_task = get_client.post("/add_task", json={
        'name': 'task_1',
        'executor_id': 1,
        'dedline': '2026-04-15',
        'description': 'Описание задачи'
        })
        response = get_client.post("/add_message", json={
            "task_id": 1,
            "message": 'message for task 1'
        })
        assert response.status_code == 200
    
    def test_update_task(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'менеджер'})
        add_task = get_client.post("/add_task", json={
        'name': 'task_1',
        'executor_id': 1,
        'dedline': '2026-04-15',
        'description': 'Описание задачи'
        })

        response = get_client.patch("/update_task", json={
            'id': 1,
            'new_name': 'New nama task 1',
            'executor_id': 2,
            'status': 'в работе',
            'dedline': '2026-04-25',
            'description': 'Новое Описание задачи'
        })
        assert response.status_code == 200

    def test_delete_task(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
        add_user_to_team = get_client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'менеджер'})
        add_task = get_client.post("/add_task", json={
        'name': 'task_1',
        'executor_id': 1,
        'dedline': '2026-04-15',
        'description': 'Описание задачи'
        })
        #  реализовать
# @router.delete('/delete_task')
# async def delete_task(data_task: TaskDeleteSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
#     check_user_admin(user_data.role)
#     task = db.query(TaskModel).filter(TaskModel.id == data_task.id, TaskModel.executor_id == data_task.executor_id, TaskModel.team_id == user_data.team_id).first()
#     check_absence_task(task)
#     task_delete_db(db=db, task=task)
#     return {'message': f'Задача {task.name} удалена'}


    def test_job_evaluation(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        response = get_client.patch("/job_evaluation", json={
            'id': 1,
            'name': 'New nama task 1',
            'job_evaluation': 5
        })
        assert response.status_code == 200
        response = get_client.patch("/job_evaluation", json={
            'id': 2,
            'name': 'task_1',
            'job_evaluation': 6
        })
        assert response.status_code == 404

    def test_get_task_user(self, get_client, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
        response = get_client.get('/task_user/1')
        assert response.status_code == 200
        response = get_client.get('/task_user/2')
        assert response.status_code == 200
        # response = get_client.get('/task_user/3')
        # assert response.status_code == 200

