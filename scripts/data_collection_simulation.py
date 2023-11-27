import os
from google.cloud import storage
import pandas as pd
from datetime import datetime

def download_data_from_gcs(bucket_name, source_blob_name, destination_file_path, key_path):
    """Download a file from Google Cloud Storage."""
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_path)

def simulate_weekly_data_collection():
    """
    Assuming the source data will be available weekly under the secured GCP bucket "dcase2023bucketdataset".
    Or we can also assume and work with any server or from a url and extract the zip directly
    Simulates weekly data collection and downloads CSV files from Google Cloud Storage.
    """

    print("Starting the weekly data collection and download script...")

    # Google Cloud Storage configuration
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "dcase2023bucketdataset")
    key_path = os.environ.get("GCS_KEY_PATH", "/app/mldocker-4713e7f8b358.json")

    # Include year, month, and day in the folder structure
    current_date = datetime.now().strftime("%Y/%m/%d")
    destination_folder = f'/data/weekly/upload/{current_date}/'
    os.makedirs(destination_folder, exist_ok=True)

    # List of machinery types
    machinery_types = ["fan", "bearing", "gearbox", "slider", "ToyCar", "ToyTrain", "valve"]

    # Download CSV files for each machinery type
    for machinery_type in machinery_types:
        source_blob_name = f"DcaseDevDataSet/{machinery_type}/attributes_00.csv"
        destination_file_path = os.path.join(destination_folder, f'{machinery_type}_attributes_00.csv')
        download_data_from_gcs(bucket_name, source_blob_name, destination_file_path, key_path)
        print(f"Downloaded {machinery_type} data from Google Cloud Storage to {destination_file_path}")

    print("Weekly data collection and download script completed.")

if __name__ == "__main__":

    destination_file_path = 'app/data/weekly/upload'
    
    simulate_weekly_data_collection()
