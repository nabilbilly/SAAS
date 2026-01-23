from app.db.session import SessionLocal
from app.modules.evoucher.service import EVoucherService
from app.modules.evoucher.schemas import EVoucherCreate
from datetime import datetime

def reproduce_error():
    db = SessionLocal()
    try:
        data = EVoucherCreate(
            academic_year_id=1,
            count=1,
            expires_at=datetime.utcnow()
        )
        print("Attempting to create voucher...")
        # Call the service method directly
        service = EVoucherService()
        # Mocking the internal call logic to debug specific part
        from app.core.security import get_password_hash
        pin = "123456"
        print(f"Hashing PIN: '{pin}' (Type: {type(pin)})")
        try:
            h = get_password_hash(pin)
            print(f"Hash success: {h}")
        except Exception as e:
             print(f"Hash FAILED: {e}")
        
        result = service.create_vouchers(db, data)
        print("Success!", result)
    except Exception as e:
        print(f"FAILED with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    reproduce_error()
