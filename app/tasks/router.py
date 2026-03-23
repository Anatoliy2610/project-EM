from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from typing import List
from sqlalchemy.orm import Session, selectinload
from datetime import datetime

from app.tasks.models import TaskModel
from app.tasks.schemas import EvaluationSchema, JobResultSchema, TaskAddUpdateSchema, TaskDeleteSchema, TaskSchema
# from app.users.models import UserModel

from app.config import get_current_user, get_db
from app.users.models import UserModel
from app.config import templates


router = APIRouter(tags=['Задачи'])



# ### 3. Задачи
# - Создание задач руководителем
# - Назначение исполнителя
# - Описание, дедлайн, статус
# - Изменение / удаление
# - Комментарии (упрощённый чат внутри задачи)
# - Статусы: открыто, в работе, выполнено



# @router.get("/tasks", response_model=List[TaskSchema])
@router.get("/tasks")
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    data_tasks = db.query(TaskModel).options(
        selectinload(TaskModel.executor),
        selectinload(TaskModel.team),
    ).all()
    return templates.TemplateResponse(
        request=request, name="tasks/tasks.html", context={"data_tasks": data_tasks}
    )


@router.post("/add_task")
async def add_tasks(data_task: TaskAddUpdateSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    executor = db.query(UserModel).filter(UserModel.id == data_task.executor_id, UserModel.team_id == user_data.team_id).first()
    if not executor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Исполнитель не в вашей команде'
        )
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.executor_id == data_task.executor_id).first()
    if task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Задача с таким названием для исполнителя существует'
        )
    db_task = TaskModel(
        name = data_task.name,
        executor_id = executor,
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
    return {'message': f'Задача зарегистрирована для {executor.email}'}


@router.patch('/update_task')
async def update_task(data_task: TaskAddUpdateSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.executor_id == data_task.executor_id, TaskModel.team_id == user_data.team_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такой задачи не существует'
        )
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
    return {'message': f'Задача {data_task.name} изменена'}


@router.delete('/delete_task')
async def delete_task(data_task: TaskDeleteSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.executor_id == data_task.executor_id, TaskModel.team_id == user_data.team_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такой задачи не существует'
        )
    db.delete(task)
    db.commit()
    return {'message': f'Задача {data_task.name} удалена'}



@router.patch('/job_evaluation')
async def job_evaluation(data_task: EvaluationSchema, user_data: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_data.role != 'админ команды':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У Вас не достаточно прав'
        )
    task = db.query(TaskModel).filter(TaskModel.name == data_task.name, TaskModel.team_id == user_data.team_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такой задачи не существует'
        )
    if data_task.job_evaluation == 5:
        task.job_evaluation = data_task.job_evaluation
        task.status = 'выполнена'
    else:
        task.job_evaluation = data_task.job_evaluation
        task.status = 'в работе'
    db.commit()
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


# ### 6. Календарь
# - Простое отображение задач и встреч по дням
# - Месячный и дневной вид в виде текстовой таблицы
# - Автоматическое добавление задач и встреч


