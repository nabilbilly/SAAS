import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_generate_vouchers():
    url = f"{BASE_URL}/evoucher/admin/vouchers"
    payload = {
        "academic_year_id": 1,
        "count": 5,
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    try:
        print(f"Sending POST to {url} with payload {payload}")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("SUCCESS: Vouchers generated.")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_generate_vouchers()
