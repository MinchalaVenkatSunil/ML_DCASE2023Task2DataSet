import logging
import os
import requests
import base64
from google.auth.transport.requests import Request
from google.oauth2 import service_account

logging.basicConfig(
    filename='data_transfer_to_gcs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# TODO: Use another alternative authentication in GCP
def get_access_token(json_key_path):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            json_key_path,
            scopes=('https://www.googleapis.com/auth/cloud-platform',),
        )

        credentials.refresh(Request())
        access_token = credentials.token

        return access_token
    except Exception as e:
        logging.error(f"Error obtaining access token: {str(e)}")

def transfer_weekly_data_to_gcs(
        local_data_path, 
        gcp_function_url):
    """Transfer locally collected data to Google Cloud Storage via Google Cloud Function."""
    logging.info("Venkat Starting weekly data transfer to Google Cloud Storage...")

    # Obtain access token
    # json_key_path = "C:/Users/harit/Documents/Visual Studio 2022/MLDockerTest/Dcase2023Dataset/mldocker-key-gcp.json"
    json_key_path = "/app/mldocker-key-gcp.json"
    access_token = get_access_token(json_key_path)

    # Set up headers for the request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    try:
        local_files = [f for f in os.listdir(local_data_path) if os.path.isfile(os.path.join(local_data_path, f))]

        for local_file in local_files:
            local_file_path = os.path.join(local_data_path, local_file)

            with open(local_file_path, 'rb') as file:
                content = file.read()

            # Base64 encode the content
            content_base64 = base64.b64encode(content).decode('utf-8')

            # Prepare data payload for the Google Cloud Function
            data = {
                'file_name': local_file,
                'content': content_base64
            }

            # Send data to Google Cloud Function
            response = requests.post(gcp_function_url, json=data, headers=headers)

            # Check the response status code
            if response.status_code == 401:
                logging.error("Unauthorized request. Check your authorization credentials.")
            else:
                logging.info(f"Successfully transferred data: {data.get('file_name')}, Response: {response.text}")

        logging.info("Weekly data transfer to Google Cloud Storage completed.")
    except Exception as e:
        logging.error(f"Error during data transfer: {str(e)}")

if __name__ == "__main__":
    # local_data_path = "C:/Users/harit/Documents/temp/result/result"
    local_data_path = "/app/result"
    gcp_function_url = "https://europe-north1-mldocker.cloudfunctions.net/process_data"

    transfer_weekly_data_to_gcs(
        local_data_path, 
        gcp_function_url)
