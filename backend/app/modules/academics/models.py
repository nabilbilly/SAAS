from sqlalchemy import Column, Integer, String, Date, Enum as SqlEnum
import enum
from app.db.base import Base

class YearStatus(str, enum.Enum):
    ACTIVE = "Active"
    DRAFT = "Draft"
    ARCHIVED = "Archived"

class AcademicYear(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g., 2026/2027
    status = Column(SqlEnum(YearStatus), default=YearStatus.DRAFT)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
