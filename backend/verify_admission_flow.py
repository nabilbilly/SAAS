import requests
import sys
import time
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_admission_flow():
    print("Starting Admission Flow Verification...")
    
    # 1. Setup: Create Academic Year, Term, Class, Stream
    print("\n1. Setting up prerequisites...")
    year_data = {
        "name": f"Test Year {int(time.time())}",
        "status": "Active",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31"
    }
    print(f"Creating Academic Year with data: {year_data}")
    try:
        r = requests.post(f"{BASE_URL}/academics/", json=year_data, timeout=10)
    except Exception as e:
        print(f"Request failed: {e}")
        return
    if r.status_code != 200:
        print(f"Failed to create year: {r.text}")
        return
    year = r.json()
    year_id = year['id']
    print(f"Academic Year created: {year['name']} (ID: {year_id})")

    term_data = {
        "name": "Term 1",
        "status": "Active",
        "sequence": 1,
        "start_date": "2026-01-01",
        "end_date": "2026-04-30"
    }
    r = requests.post(f"{BASE_URL}/academics/{year_id}/terms", json=term_data)
    term = r.json()
    term_id = term['id']
    print(f"Term created: {term['name']} (ID: {term_id})")

    class_data = {
        "name": f"JHS 1 {int(time.time())}",
        "level": "JHS"
    }
    r = requests.post(f"{BASE_URL}/academics/classes", json=class_data)
    class_room = r.json()
    class_id = class_room['id']
    print(f"Class created: {class_room['name']} (ID: {class_id})")

    stream_data = {
        "class_id": class_id,
        "name": "Gold"
    }
    r = requests.post(f"{BASE_URL}/academics/streams", json=stream_data)
    stream = r.json()
    stream_id = stream['id']
    print(f"Stream created: {stream['name']} (ID: {stream_id})")

    # 2. Create Voucher
    print("\n2. Creating test voucher...")
    v_data = {
        "academic_year_id": year_id,
        "count": 1,
        "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    r = requests.post(f"{BASE_URL}/evoucher/admin/vouchers", json=v_data)
    voucher_info = r.json()[0]
    print(f"Voucher created: {voucher_info['voucher_number']}, PIN: {voucher_info['pin']}")

    # 3. Step 1: Verify Voucher
    print("\n3. Verifying voucher (Step 1)...")
    verify_data = {
        "voucher_number": voucher_info['voucher_number'],
        "pin": voucher_info['pin']
    }
    r = requests.post(f"{BASE_URL}/evoucher/verify", json=verify_data)
    verify_res = r.json()
    if not verify_res['valid']:
        print(f"Voucher verification failed: {verify_res}")
        return
    session_token = verify_res['voucher_session_token']
    print(f"Voucher verified! Session Token: {session_token}")

    # 4. Step 2-3: Submit Admission (Pending)
    print("\n4. Submitting pending admission (Step 2-3)...")
    admission_submit = {
        "voucher_session_token": session_token,
        "student": {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male",
            "date_of_birth": "2015-05-20",
            "nationality": "Ghanaian"
        },
        "guardians": [
            {
                "name": "Jane Doe",
                "relationship_type": "Mother",
                "phone": "0240000000",
                "address": "123 School St"
            }
        ],
        "medical": {
            "health_conditions": "None",
            "allergies": "Peanuts"
        },
        "placement": {
            "academic_year_id": year_id,
            "class_id": class_id,
            "stream_id": stream_id,
            "term_id": term_id
        }
    }
    r = requests.post(f"{BASE_URL}/admissions/", json=admission_submit)
    if r.status_code != 200:
        print(f"Admission submission failed: {r.text}")
        return
    admission = r.json()
    admission_id = admission['id']
    print(f"Pending Admission created! ID: {admission_id}, Status: {admission['status']}")

    # 5. Step 4: Approve Admission
    print("\n5. Approving admission (Step 4)...")
    r = requests.post(f"{BASE_URL}/admissions/{admission_id}/approve")
    if r.status_code != 200:
        print(f"Admission approval failed: {r.text}")
        return
    final_admission = r.json()
    print(f"Admission APPROVED! Status: {final_admission['status']}")
    print(f"Approved At: {final_admission['approved_at']}")

    # 6. Final Verification
    print("\n6. Running final checks...")
    
    # Check student for index number
    student_id = final_admission['student_id']
    r = requests.get(f"{BASE_URL}/students/{student_id}")
    student = r.json()
    print(f"Student Index Number: {student['index_number']}")
    if not student['index_number']:
        print("FAIL: Index number not generated!")
    
    # Check account status
    if student['account']['is_active']:
        print("Student Account is ACTIVE.")
    else:
        print("FAIL: Student account is NOT active!")

    print("\nVerification COMPLETE!")

if __name__ == "__main__":
    test_admission_flow()
