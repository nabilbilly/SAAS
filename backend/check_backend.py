import requests
import sys

def check_health():
    urls = [
        "http://localhost:8000/health",
        "http://127.0.0.1:8000/health",
        "http://localhost:8000/api/v1/academics/"
    ]
    
    for url in urls:
        print(f"Checking {url}...")
        try:
            r = requests.get(url, timeout=5)
            print(f"  Status: {r.status_code}")
            print(f"  Response: {r.text[:100]}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    check_health()
