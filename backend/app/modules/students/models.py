from sqlalchemy import Column, Integer, String, Date, Enum as SqlEnum, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.db.base import Base

class Gender(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"

class Student(Base):
    id = Column(Integer, primary_key=True, index=True)
    index_number = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    gender = Column(SqlEnum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    nationality = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    photo = Column(String, nullable=True) # File path
    created_at = Column(DateTime, default=datetime.utcnow)

    guardians = relationship("Guardian", back_populates="student", cascade="all, delete-orphan")
    medical = relationship("StudentMedical", back_populates="student", uselist=False, cascade="all, delete-orphan")
    account = relationship("StudentAccount", back_populates="student", uselist=False, cascade="all, delete-orphan")
    admissions = relationship("Admission", back_populates="student")

class Guardian(Base):
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    relationship_type = Column(String, nullable=False) # e.g. Father, Mother
    phone = Column(String, nullable=False)
    secondary_phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=False)
    occupation = Column(String, nullable=True)

    student = relationship("Student", back_populates="guardians")

class StudentMedical(Base):
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    health_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    special_needs = Column(Text, nullable=True)

    student = relationship("Student", back_populates="medical")

class StudentAccount(Base):
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    must_change_password = Column(Boolean, default=True)
    is_active = Column(Boolean, default=False)

    student = relationship("Student", back_populates="account")
