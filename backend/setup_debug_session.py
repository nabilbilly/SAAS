import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def create_debug_session():
    # 1. Get an active academic year
    print("Fetching academic years...")
    r = requests.get(f"{BASE_URL}/academics/")
    years = r.json()
    if not years:
        print("No academic years found. Setup required.")
        return
    
    # Find active or just use the first one
    year_id = years[0]['id']
    print(f"Using Academic Year ID: {year_id}")

    # 2. Create a voucher
    print("Creating a voucher...")
    v_payload = {
        "academic_year_id": year_id,
        "count": 1,
        "expires_at": "2027-12-31T23:59:59"
    }
    r = requests.post(f"{BASE_URL}/evoucher/admin/vouchers", json=v_payload)
    if r.status_code != 200:
        print(f"Failed to create voucher: {r.text}")
        return
    
    voucher = r.json()[0]
    v_num = voucher['voucher_number']
    v_pin = voucher['pin']
    print(f"Voucher Created: {v_num} / {v_pin}")

    # 3. Verify it to get a session token
    print("Verifying voucher...")
    verify_payload = {
        "voucher_number": v_num,
        "pin": v_pin
    }
    r = requests.post(f"{BASE_URL}/evoucher/verify", json=verify_payload)
    if r.status_code != 200:
        print(f"Failed to verify: {r.text}")
        return
    
    res = r.json()
    if res.get('valid'):
        print("\nSUCCESS! Use this session token in your browser console:")
        print(f"sessionStorage.setItem('admission_voucher_token', '{res['voucher_session_token']}')")
        print("\nThen navigate to: http://localhost:5173/admission/form")
    else:
        print(f"Verification failed: {res}")

if __name__ == "__main__":
    create_debug_session()
