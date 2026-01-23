from pydantic import BaseModel
from datetime import date
from .models import YearStatus

class AcademicYearBase(BaseModel):
    name: str
    status: YearStatus
    start_date: date | None = None
    end_date: date | None = None

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearUpdate(BaseModel):
    name: str | None = None
    status: YearStatus | None = None
    start_date: date | None = None
    end_date: date | None = None

class AcademicYearResponse(AcademicYearBase):
    id: int

    class Config:
        from_attributes = True
