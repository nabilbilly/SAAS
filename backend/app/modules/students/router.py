from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer
from . import schemas, models
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from jose import jwt, JWTError

router = APIRouter()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/students/login"
)

def get_current_student(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> models.Student:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    student = db.query(models.Student).filter(
        models.Student.account.has(username=username)
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/login", response_model=schemas.Token)
def student_login(
    obj_in: schemas.StudentLogin,
    db: Session = Depends(get_db)
):
    # Search by index_number OR username
    student = db.query(models.Student).filter(
        (models.Student.index_number == obj_in.username) |
        (models.Student.account.has(username=obj_in.username))
    ).first()

    if not student or not student.account:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not student.account.is_active:
        raise HTTPException(status_code=401, detail="Account is inactive. Please contact admin.")

    if not verify_password(obj_in.password, student.account.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": student.account.username, "id": student.id, "type": "student"}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "must_change_password": student.account.must_change_password,
        "student_name": f"{student.first_name} {student.last_name}",
        "index_number": student.index_number or "N/A"
    }

@router.post("/change-password")
def change_password(
    obj_in: schemas.StudentPasswordChange,
    current_student: models.Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    if not verify_password(obj_in.current_password, current_student.account.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    current_student.account.hashed_password = get_password_hash(obj_in.new_password)
    current_student.account.must_change_password = False
    
    db.commit()
    return {"message": "Password changed successfully", "success": True}

@router.get("/", response_model=List[schemas.StudentResponse])
def list_students(
    db: Session = Depends(get_db)
):
    return db.query(models.Student).all()

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    obj_in: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    return student
