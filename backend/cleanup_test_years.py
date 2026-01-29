import requests

BASE_URL = "http://localhost:8000/api/v1/academics"

def cleanup():
    r = requests.get(f"{BASE_URL}/")
    years = r.json()
    
    for year in years:
        name = year['name']
        year_id = year['id']
        
        # Check if it's a test year
        if name.startswith("Test Year"):
            print(f"Deleting {name} (ID: {year_id})...")
            
            # First, check for terms and delete them if they exist
            # (Though my delete endpoint might handle it or fail if RESTRUCT is on)
            # Fetch terms first
            terms_r = requests.get(f"{BASE_URL}/{year_id}/terms")
            if terms_r.status_code == 200:
                for term in terms_r.json():
                    requests.delete(f"{BASE_URL}/terms/{term['id']}")
            
            # Now delete the year
            dr = requests.delete(f"{BASE_URL}/{year_id}")
            if dr.status_code == 200:
                print(f"Successfully deleted {name}")
            else:
                print(f"Failed to delete {name}: {dr.status_code} - {dr.text}")

if __name__ == "__main__":
    cleanup()
