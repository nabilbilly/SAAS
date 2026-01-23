import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def list_years():
    res = requests.get(f"{BASE_URL}/academics/")
    if res.status_code == 200:
        years = res.json()
        print(f"Found {len(years)} years:")
        for y in years:
            print(f"ID: {y['id']}, Name: {y['name']}, Status: {y['status']}, Start: {y.get('start_date')}, End: {y.get('end_date')}")
            if y['status'] == 'Active':
                 print("!!! ACTIVE YEAR FOUND !!!")
    else:
        print(res.text)

if __name__ == "__main__":
    list_years()
