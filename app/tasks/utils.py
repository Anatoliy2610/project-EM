from datetime import datetime

from fastapi import HTTPException, status

from app.tasks.models import TaskModel


def check_user_admin(user_role):
    if user_role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У Вас не достаточно прав'
        )
    
    
def check_user(user):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователя не существует'
        )
    
def check_availability_task(task):
    if task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Задача с таким названием для исполнителя существует'
        )
def check_absence_task(task):
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой задачи не существует'
        )

    
def check_executor(executor):
    if not executor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Исполнитель не в вашей команде'
        )


def task_add_db(data_task, executor, db):
    print(data_task.dict())
    db_task = TaskModel(
        name = data_task.name,
        executor_id = executor.id,
        status = data_task.status if data_task.status else 'открыто',
        dedline = datetime(
            int(data_task.dedline.split('-')[0]),
            int(data_task.dedline.split('-')[1]),
            int(data_task.dedline.split('-')[2]),
        ),
        description = data_task.description,
        chat = data_task.chat,
        team_id = executor.team_id
        )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)


def task_update_db(data_task, db, task):
    if data_task.new_name:
        task.name = data_task.new_name
    if data_task.executor_id:
        task.executor_id = data_task.executor_id
    if data_task.status:
        task.status = data_task.status
    if data_task.dedline:
        task.dedline = datetime(
            int(data_task.dedline.split('-')[0]),
            int(data_task.dedline.split('-')[1]),
            int(data_task.dedline.split('-')[2]),
        )
    if data_task.description:
        task.description = data_task.description
    if data_task.chat:
        task.chat = data_task.chat
    db.commit()


def task_delete_db(db, task):
    db.delete(task)
    db.commit()


def add_evaluation_db(job_evaluation, task, db):
    if job_evaluation not in range(1, 6):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Оценка должны быть от 1 до 5'
        )
    if job_evaluation == 5:
        task.job_evaluation = job_evaluation
        task.status = 'выполнена'
    else:
        task.job_evaluation = job_evaluation
        task.status = 'в работе'
    db.commit()
