from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from . import schemas, models
from app.modules.evoucher.models import EVoucher

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
def update_academic_year(
    year_id: int,
    obj_in: schemas.AcademicYearUpdate,
    db: Session = Depends(get_db)
):
    year = db.query(models.AcademicYear).filter(models.AcademicYear.id == year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")
    
    # Update fields
    if obj_in.name is not None:
        year.name = obj_in.name
    if obj_in.start_date is not None:
        year.start_date = obj_in.start_date
    if obj_in.end_date is not None:
        year.end_date = obj_in.end_date
    
    # Handle status change logic
    if obj_in.status is not None:
        if obj_in.status == models.YearStatus.ACTIVE:
            # Validate dates
            start = obj_in.start_date if obj_in.start_date is not None else year.start_date
            end = obj_in.end_date if obj_in.end_date is not None else year.end_date
            
            if not start or not end:
                raise HTTPException(status_code=400, detail="Start date and end date are required to activate academic year")
            if start >= end:
                raise HTTPException(status_code=400, detail="Start date must be before end date")
            
            # Check for other active years
            active_year = db.query(models.AcademicYear).filter(
                models.AcademicYear.status == models.YearStatus.ACTIVE,
                models.AcademicYear.id != year_id
            ).first()
            if active_year:
                raise HTTPException(status_code=400, detail="Another academic year is already active")
        
        year.status = obj_in.status

    db.commit()
    db.refresh(year)
    return year

@router.delete("/{year_id}")
def delete_academic_year(
    year_id: int,
    db: Session = Depends(get_db)
):
    year = db.query(models.AcademicYear).filter(models.AcademicYear.id == year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail="Year not found")
    
    # Safety Check: Prevent deleting active year
    if year.status == models.YearStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Cannot delete an Active academic year. Archive it first.")
    
    # Dependency Check: Check for associated vouchers
    vouchers = db.query(EVoucher).filter(EVoucher.academic_year_id == year_id).first()
    if vouchers:
        raise HTTPException(status_code=400, detail="Cannot delete academic year: Associated vouchers exist.")
    
    db.delete(year)
    db.commit()
    return {"message": "Academic year deleted successfully"}
