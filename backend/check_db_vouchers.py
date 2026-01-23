from app.db.session import SessionLocal
from app.modules.evoucher.models import EVoucher
from app.core.config import settings

def check_db_content():
    print(f"Checking Database: {settings.POSTGRES_DB}")
    print(f"URL: {settings.sqlalchemy_database_uri}")
    
    db = SessionLocal()
    try:
        count = db.query(EVoucher).count()
        print(f"Total Vouchers found in '{settings.POSTGRES_DB}': {count}")
        
        vouchers = db.query(EVoucher).limit(5).all()
        for v in vouchers:
            print(f"- {v.voucher_number} (Status: {v.status})")
    finally:
        db.close()

if __name__ == "__main__":
    check_db_content()
