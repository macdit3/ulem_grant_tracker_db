import requests
import json
from pprint import pprint

# Base URL for the API
BASE_URL = "https://ulem-grant-tracker-db.onrender.com"

def print_response(response, endpoint):
    """Helper function to print the response in a readable format"""
    print(f"\n{'='*50}")
    print(f"Testing endpoint: {endpoint}")
    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        try:
            # Pretty print the JSON response
            pprint(response.json())
        except json.JSONDecodeError:
            print("Response is not in JSON format:")
            print(response.text)
    else:
        print(f"Error response: {response.text}")

    print(f"{'='*50}\n")

def main():
    """Main function to run all HTTP requests"""

    # Define headers
    headers = {
        "Accept": "application/json"
    }

    # Test GET donations endpoint
    endpoint = "/donations/"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)

    # Test GET donors endpoint
    endpoint = "/donors/"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)

    # Test GET pledges endpoint
    endpoint = "/pledges/"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)

    # Test GET programs endpoint
    endpoint = "/programs/"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)

    # Test GET tax-receipts endpoint with ID 2
    endpoint = "/tax-receipts/2"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)

    # Test GET pending thank you notes endpoint
    endpoint = "/reports/pending-thank-you-notes/"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)

if __name__ == "__main__":
    print("Starting API endpoint tests...")
    main()
    print("API endpoint tests completed.")