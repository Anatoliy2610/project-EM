from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session, selectinload
from datetime import datetime

from app.tasks.models import MessageModel, TaskModel
from app.tasks.schemas import ChatSchema, MessageAddSchema, EvaluationSchema, JobResultSchema, TaskAddUpdateSchema, TaskDeleteSchema, TaskSchema
# from app.users.models import UserModel

from app.config import get_current_user, get_db
from app.tasks.utils import add_evaluation_db, add_message_db, check_absence_task, check_availability_task, check_executor, check_user_admin, get_messages, task_add_db, task_delete_db, task_update_db
from app.users.models import UserModel
from app.config import templates


router = APIRouter(tags=['Задачи'])


# @router.get("/tasks", response_model=List[TaskSchema])
@router.get("/tasks")
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    data_tasks = db.query(TaskModel).options(
        selectinload(TaskModel.executor),
        selectinload(TaskModel.team),
        selectinload(TaskModel.chat)
    ).all()
    return templates.TemplateResponse(
        request=request, name="tasks/tasks.html", context={"data_tasks": data_tasks}
    )


@router.post("/add_task")
async def add_task(data_task: TaskAddUpdateSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "name": "string",
    "new_name": "string",
    "executor_id": 0,
    "status": "string",
    "dedline": "string",
    "description": "string"
    }
    '''
    check_user_admin(user_data.role)
    executor = db.query(UserModel).filter(UserModel.id == data_task.executor_id, UserModel.team_id == user_data.team_id).first()
    check_executor(executor)
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.executor_id == data_task.executor_id).first()
    check_availability_task(task)
    task_add_db(data_task=data_task, executor=executor, db=db)
    return {'message': f'Задача зарегистрирована для {executor.email}'}



@router.post("/add_message")
async def add_message_chat(data_chat: MessageAddSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == data_chat.task_id, TaskModel.team_id == user_data.team_id).first()
    check_absence_task(task=task)
    add_message_db(data_chat=data_chat, user_data=user_data, task=task, db=db)
    return {'message': f'Добавлено сообщение в чат к задаче {task.name}'}


@router.get("/get_chat")
async def get_chat(data_chat: ChatSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role == 'админ команды':
        task = db.query(TaskModel).filter(TaskModel.id == data_chat.task_id, TaskModel.team_id == user_data.team_id).first()
    else:
        task = db.query(TaskModel).filter(TaskModel.id == data_chat.task_id, TaskModel.executor_id == user_data.id).first()
    chat = get_messages(task)
    if chat:
        return {'message': f'Чат для Админа по задаче {task.name} - {chat}'}
    return {'message': 'Сообщений по данной задаче нет'}
    

@router.patch('/update_task')
async def update_task(data_task: TaskAddUpdateSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "name": "string",
    "new_name": "string",
    "executor_id": 0,
    "status": "string",
    "dedline": "string",
    "description": "string",
    "chat": "string"
    }
    '''
    check_user_admin(user_data.role)
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.executor_id == data_task.executor_id, TaskModel.team_id == user_data.team_id).first()
    check_absence_task(task)
    task_update_db(data_task=data_task, db=db, task=task)
    return {'message': f'Задача {data_task.name} изменена'}


@router.delete('/delete_task')
async def delete_task(data_task: TaskDeleteSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "name": "string",
    "executor_id": 0
    }
    '''
    check_user_admin(user_data.role)
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.executor_id == data_task.executor_id, TaskModel.team_id == user_data.team_id).first()
    check_absence_task(task)
    task_delete_db(db=db, task=task)
    return {'message': f'Задача {data_task.name} удалена'}



@router.patch('/job_evaluation')
async def job_evaluation(data_task: EvaluationSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    {
    "name": "string",
    "job_evaluation": 0
    }
    '''
    check_user_admin(user_data.role)
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.team_id == user_data.team_id).first()
    check_absence_task(task)
    add_evaluation_db(
        job_evaluation=data_task.job_evaluation,
        task=task,
        db=db
        )
    return {'message': f'Задача {data_task.name} выполнена на {data_task.job_evaluation} баллов'}


@router.get('/job_result', response_model=List[JobResultSchema])
async def get_job_result(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    data_user = db.query(TaskModel).filter(TaskModel.executor_id == user_data.id).all()
    return data_user


@router.get('/average_grade')
async def get_average_grade(user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    data_user = db.query(TaskModel).filter(TaskModel.executor_id == user_data.id).all()
    if data_user:
        res_sum = 0
        res_len = 0
        for data in data_user:
            if data.job_evaluation:
                res_sum += data.job_evaluation
                res_len += 1
        if res_len == 0:
            return {"message": f"У пользователя {user_data.email} нет задач c оценками"}
        average_grade = res_sum / res_len
        return {"message": f"Средняя оценка по задачам у пользователя {user_data.email} - '{average_grade}'"}
    return {"message": f"У пользователя {user_data.email} нет задач"}
