from pydantic import BaseModel
from .models import YearStatus

class AcademicYearBase(BaseModel):
    name: str
    status: YearStatus

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearResponse(AcademicYearBase):
    id: int

    class Config:
        from_attributes = True
