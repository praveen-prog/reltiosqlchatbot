import requests
import base64
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables for credentials and endpoints
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
base_url = os.getenv("base_url")
patient_data_endpoint = os.getenv("patient_data_endpoint")

# Reltio OAuth URL
auth_url = "https://auth.reltio.com/oauth/token"

# Encode client ID and client secret in Base64
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Define headers for the OAuth request
auth_headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded",
}

# Payload for OAuth token request with 'client_credentials' grant type
auth_payload = {
    "grant_type": "client_credentials",
}

# Function to retrieve OAuth token
def get_oauth_token():
    try:
        response = requests.post(auth_url, headers=auth_headers, data=auth_payload)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print("Access token retrieved successfully.")
            return access_token
        else:
            print(f"Failed to retrieve access token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving the access token: {e}")
        return None

# Function to get data from Reltio using OAuth token and handle pagination
def get_reltio_data():
    access_token = get_oauth_token()
    if not access_token:
        print("Unable to retrieve data due to missing access token.")
        return

    # Set up headers with the Bearer token for the data request
    data_headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Construct the initial data endpoint URL
    #data_endpoint = f"{base_url}/entities?filter=(equals(type,'{patient_data_endpoint}'))"
    data_endpoint = f"{base_url}/entities?filter=(equals(type,'{patient_data_endpoint}'))&pageSize=10000"
    cursor = None
    all_records = []

    try:
        while True:
            if cursor:
                paginated_endpoint = f"{data_endpoint}&cursor={cursor}"
            else:
                paginated_endpoint = data_endpoint

            response = requests.get(paginated_endpoint, headers=data_headers)
            if response.status_code == 200:
                data = response.json()
                print("Data retrieved successfully.")

                # Ensure data is a list
                if isinstance(data, list):
                    all_records.extend(data)
                else:
                    print("Unexpected data format.")
                    break

                # Check if more pages are available
                cursor = response.headers.get("Next-Page-Cursor")
                if not cursor:
                    break  # Exit loop if no more pages

            else:
                print(f"Failed to retrieve data: {response.status_code} - {response.text}")
                break

        # Write all records to CSV
        if all_records:
            with open("outputjson.csv", mode="w", newline="") as file:
                headers = all_records[0].keys() if all_records else []
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(all_records)
                print("Data written to outputjson.csv successfully.")
        else:
            print("No records found.")

    except Exception as e:
        print(f"An error occurred while retrieving data: {e}")

# Call the function to get data and write to CSV
get_reltio_data()
