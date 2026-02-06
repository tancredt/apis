import requests
from pprint import pprint
import os
import sys

# Add the project directory to Python path so we can import Django settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def login_to_api(username, password, base_url='http://localhost:8000'):
    """
    Function to login to the Django API using requests
    """
    # Session object to persist cookies
    session = requests.Session()

    # Note: The login endpoint is decorated with @csrf_exempt, so we don't need CSRF token for login
    # But we might need it for other requests

    # Step 1: Perform login (without CSRF token since login endpoint is csrf_exempt)
    print("Step 1: Attempting login...")
    login_url = f"{base_url}/inventory/auth/login/"

    headers = {
        'Content-Type': 'application/json',
        'Referer': base_url,  # Sometimes required by Django
    }

    # Login payload
    login_data = {
        'username': username,
        'password': password
    }

    # Make the login request
    login_response = session.post(
        login_url,
        json=login_data,
        headers=headers
    )

    print(f"Login response status: {login_response.status_code}")
    print(f"Login response headers: {dict(login_response.headers)}")

    if login_response.status_code == 200:
        response_data = login_response.json()
        print(f"Login successful: {response_data}")

        # Step 2: Test accessing a protected endpoint
        print("\nStep 2: Testing access to protected endpoint...")
        protected_response = session.get(f"{base_url}/inventory/auth/current-user/")
        print(f"Protected endpoint status: {protected_response.status_code}")
        if protected_response.status_code == 200:
            print(f"Current user: {protected_response.json()}")
        else:
            print(f"Could not access protected endpoint: {protected_response.status_code}")

        return session, response_data
    else:
        print(f"Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")

        # Let's try without any special headers to see if that's the issue
        print("\nTrying again without extra headers...")
        minimal_headers = {'Content-Type': 'application/json'}
        login_response_minimal = session.post(
            login_url,
            json=login_data,
            headers=minimal_headers
        )

        print(f"Minimal headers response status: {login_response_minimal.status_code}")
        print(f"Minimal headers response: {login_response_minimal.text}")

        return None, login_response.text

def test_login():
    """
    Test function to demonstrate the login process
    """
    # Get credentials from environment variables or prompt user
    username = os.getenv('DJANGO_USERNAME') or input("Enter username: ")
    password = os.getenv('DJANGO_PASSWORD') or input("Enter password: ")
    base_url = os.getenv('DJANGO_BASE_URL', 'http://localhost:8000')
    
    session, result = login_to_api(username, password, base_url)
    
    if session:
        print("\nLogin successful! Session cookies:", session.cookies.get_dict())
        
        # You can now use the session object to make authenticated requests
        # Example: Get detectors
        print("\nTrying to get detectors...")
        detectors_response = session.get(f"{base_url}/inventory/detectors/")
        print(f"Detectors response: {detectors_response.status_code}")
        
        if detectors_response.status_code == 200:
            detectors = detectors_response.json()
            print(f"Number of detectors: {len(detectors)}")
        else:
            print(f"Could not get detectors: {detectors_response.text}")
            
        # Example: Create a new detector (if you want to test POST requests)
        # Uncomment the following to test creating a detector (adjust data as needed)
        """
        print("\nTrying to create a detector...")
        new_detector_data = {
            "label": "TEST001",
            "serial": "TESTSERIAL001",
            "status": "IS",  # In Stock
            "location": 1,  # Assuming location ID 1 exists
            "detector_model": 1  # Assuming detector model ID 1 exists
        }
        create_response = session.post(f"{base_url}/inventory/detectors/", json=new_detector_data)
        print(f"Create detector response: {create_response.status_code}")
        if create_response.status_code == 201:
            print(f"New detector created: {create_response.json()}")
        else:
            print(f"Could not create detector: {create_response.text}")
        """
        
    else:
        print("\nLogin failed!")
        print("Possible issues:")
        print("- Incorrect username/password")
        print("- CSRF token not properly handled")
        print("- Session authentication not configured correctly")
        print("- Missing CORS headers in Django settings")

if __name__ == "__main__":
    test_login()