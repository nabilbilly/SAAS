from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from . import schemas, service

router = APIRouter()

@router.post("/", response_model=schemas.AdmissionResponse)
def create_admission(
    obj_in: schemas.AdmissionWizardSubmit,
    db: Session = Depends(get_db)
):
    """
    Step 2-3 of Wizard: Capture all data and create a PENDING admission.
    """
    return service.AdmissionsService.create_pending_admission(
        db,
        voucher_session_token=obj_in.voucher_session_token,
        student_data=obj_in.student.model_dump(),
        guardian_data=[g.model_dump() for g in obj_in.guardians],
        medical_data=obj_in.medical.model_dump() if obj_in.medical else None,
        placement_data=obj_in.placement
    )

@router.post("/{admission_id}/approve", response_model=schemas.AdmissionResponse)
def approve_admission(
    admission_id: int,
    admin_id: int = 1, # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """
    Step 4 of Wizard (Admin Action): Official Approval.
    """
    return service.AdmissionsService.approve_admission(db, admission_id, admin_id)

@router.get("/", response_model=List[schemas.AdmissionResponse])
def list_admissions(
    status: str = None,
    class_id: int = None,
    academic_year_id: int = None,
    term_id: int = None,
    search: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(service.Admission).join(service.Admission.student)
    
    if status:
        query = query.filter(service.Admission.status == status)
    if class_id:
        query = query.filter(service.Admission.class_id == class_id)
    if academic_year_id:
        query = query.filter(service.Admission.academic_year_id == academic_year_id)
    if term_id:
        query = query.filter(service.Admission.term_id == term_id)
    if search:
        search_filter = f"%{search}%"
        # Search by student name or voucher number
        query = query.join(service.Admission.voucher).filter(
            (service.Student.first_name.ilike(search_filter)) |
            (service.Student.last_name.ilike(search_filter)) |
            (service.EVoucher.voucher_number.ilike(search_filter))
        )
    
    return query.order_by(service.Admission.created_at.desc()).all()

@router.post("/{admission_id}/reject", response_model=schemas.AdmissionResponse)
def reject_admission(
    admission_id: int,
    admin_id: int = 1, # TODO: Get from auth token
    db: Session = Depends(get_db)
):
    """
    Reject admission application.
    """
    return service.AdmissionsService.reject_admission(db, admission_id, admin_id)

@router.get("/{admission_id}", response_model=schemas.AdmissionResponse)
def get_admission(
    admission_id: int,
    db: Session = Depends(get_db)
):
    admission = db.query(service.Admission).filter(service.Admission.id == admission_id).first()
    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    return admission
