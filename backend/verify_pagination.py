import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_pagination():
    url = f"{BASE_URL}/evoucher/admin/vouchers"
    params = {"page": 1, "size": 50, "academic_year_id": 1}
    
    try:
        print(f"Sending GET to {url} with params {params}")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data Type:", type(data))
            if isinstance(data, dict):
                print("Keys:", data.keys())
            elif isinstance(data, list):
                print("Received LIST (Old API format detected!)")
                print(json.dumps(data[:1], indent=2))
        else:
            print(f"FAILED: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_pagination()
