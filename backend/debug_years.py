from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.modules.academics.models import AcademicYear

def check_years():
    db = SessionLocal()
    try:
        years = db.query(AcademicYear).all()
        print(f"Total Academic Years: {len(years)}")
        for y in years:
            print(f"ID: {y.id}, Name: {y.name}, Status: {y.status}")
    finally:
        db.close()

if __name__ == "__main__":
    check_years()
