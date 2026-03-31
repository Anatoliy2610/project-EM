# import pytest

# from tests.test_api.conftest import client




# class TestTaskAPI:
#     def test_get_tasks(self, create_db, get_fixture_db, get_fixture_current_user):
#         response = client.get("/tasks")
#         assert response.status_code == 200

#     def test_get_add_task(self, get_fixture_db, get_fixture_current_user):
#         response = client.get("/add_task")
#         assert response.status_code == 200

#     def test_add_task(self, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
#         add_user_to_team = client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
#         assert add_user_to_team.status_code == 200
#         response = client.post("/add_task", json={
#             'name': 'task_1',
#             'executor_id': 1,
#             'dedline': '2026-04-15',
#             'description': 'Описание задачи'
#         })
#         assert response.status_code == 200
#         response = client.post("/add_task", json={
#             'name': 'task_1',
#             'executor_id': 2,
#             'dedline': '2026-04-15',
#             'description': 'Описание задачи'
#         })
#         assert response.status_code == 404


#     def test_add_message_chat(self, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
#         add_user_to_team = client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
#         add_task = client.post("/add_task", json={
#         'name': 'task_1',
#         'executor_id': 1,
#         'dedline': '2026-04-15',
#         'description': 'Описание задачи'
#         })
#         response = client.post("/add_message", json={
#             "task_id": 1,
#             "message": 'message for task 1'
#         })
#         assert response.status_code == 200
    
#     def test_update_task(self, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
#         add_user_to_team = client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
#         add_user_to_team = client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'менеджер'})
#         add_task = client.post("/add_task", json={
#         'name': 'task_1',
#         'executor_id': 1,
#         'dedline': '2026-04-15',
#         'description': 'Описание задачи'
#         })

#         response = client.patch("/update_task", json={
#             'id': 1,
#             'new_name': 'New nama task 1',
#             'executor_id': 2,
#             'status': 'в работе',
#             'dedline': '2026-04-25',
#             'description': 'Новое Описание задачи'
#         })
#         assert response.status_code == 200

#     def test_delete_task(self, get_fixture_db, get_fixture_current_user_admin, add_data_for_db):
#         add_user_to_team = client.patch("/user_to_team", json={'email_user': 'User2@mail.ru', 'role': 'сотрудник'})
#         add_user_to_team = client.patch("/user_to_team", json={'email_user': 'User3@mail.ru', 'role': 'менеджер'})
#         add_task = client.post("/add_task", json={
#         'name': 'task_1',
#         'executor_id': 1,
#         'dedline': '2026-04-15',
#         'description': 'Описание задачи'
#         })
#         # не возможно реализовать
# # @router.delete('/delete_task')
# # async def delete_task(data_task: TaskDeleteSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
# #     check_user_admin(user_data.role)
# #     task = db.query(TaskModel).filter(TaskModel.id == data_task.id, TaskModel.executor_id == data_task.executor_id, TaskModel.team_id == user_data.team_id).first()
# #     check_absence_task(task)
# #     task_delete_db(db=db, task=task)
# #     return {'message': f'Задача {task.name} удалена'}




# # @router.get('/job_evaluation/{task_id}', response_model=TaskGetResponseSchema)
# # async def get_job_evaluation(task_id: int, request: Request, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
# #     check_user_admin(user_data.role)
# #     task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.team_id == user_data.team_id).first()
# #     return templates.TemplateResponse("tasks/job_evaluation.html", {"request": request, 'current_user': user_data, 'task': task})


# # @router.patch('/job_evaluation')
# # async def job_evaluation(data_task: EvaluationSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
# #     print(data_task)
# #     check_user_admin(user_data.role)
# #     task = db.query(TaskModel).filter(TaskModel.id == data_task.id, TaskModel.name == data_task.name, TaskModel.team_id == user_data.team_id).first()
# #     check_absence_task(task)
# #     add_evaluation_db(
# #         job_evaluation=data_task.job_evaluation,
# #         task=task,
# #         db=db
# #         )
# #     return {'message': f'Задача {data_task.name} выполнена на {data_task.job_evaluation} баллов'}


# # @router.get('/tasks_user', response_model=List[JobResultSchema])
# # async def get_job_result(request: Request, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
# #     tasks_user = db.query(TaskModel).filter(TaskModel.executor_id == user_data.id).all()
# #     average_grade = get_average_grade(data_user=user_data, db=db)
# #     return templates.TemplateResponse("tasks/tasks_user.html", {"request": request, 'current_user': user_data, 'tasks_user': tasks_user, 'average_grade': average_grade})


# # @router.get('/task_user/{task_id}', response_model=List[JobResultSchema])
# # async def get_task_user(task_id: int, request: Request, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
# #     task_user = db.query(TaskModel).filter(TaskModel.id == task_id).first()
# #     return templates.TemplateResponse("tasks/task.html", {"request": request, 'current_user': user_data, 'task_user': task_user, 'chat': task_user.chat[::-1]})

