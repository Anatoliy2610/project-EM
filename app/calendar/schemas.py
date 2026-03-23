from pydantic import BaseModel
from datetime import datetime


class CalendarSchemas(BaseModel):
    first_data: datetime
    second_data: datetime = None

