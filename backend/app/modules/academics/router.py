from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from . import schemas, models

router = APIRouter()

@router.post("/", response_model=schemas.AcademicYearResponse)
def create_academic_year(
    obj_in: schemas.AcademicYearCreate,
    db: Session = Depends(get_db)
):
    # Check if name already exists
    existing = db.query(models.AcademicYear).filter(models.AcademicYear.name == obj_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Academic year name already exists")
    
    db_obj = models.AcademicYear(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[schemas.AcademicYearResponse])
def list_academic_years(
    db: Session = Depends(get_db)
):
    return db.query(models.AcademicYear).all()

@router.patch("/{year_id}", response_model=schemas.AcademicYearResponse)
def update_year_status(
    year_id: int,
    status: models.YearStatus,
    db: Session = Depends(get_db)
):
    year = db.query(models.AcademicYear).filter(models.AcademicYear.id == year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")
    
    year.status = status
    db.commit()
    db.refresh(year)
    return year
