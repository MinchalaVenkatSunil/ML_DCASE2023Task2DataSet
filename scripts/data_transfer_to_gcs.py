import logging
from google.cloud import storage
import os

# TODO: Move the logging level config from here
logging.basicConfig(
    filename='data_transfer_to_gcs.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def upload_to_gcs(bucket_name, local_path, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    try:
        json_key_path = "/app/mldocker-4713e7f8b358.json"
        # json_key_path = "C:/Users/harit/Documents/Visual Studio 2022/MLDockerTest/ML_DCASE2023Task2DataSet/mldocker-4713e7f8b358.json"
        storage_client = storage.Client.from_service_account_json(json_key_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)
        logging.info(f"Uploaded file: {local_path} to {destination_blob_name}")
    except Exception as e:
        logging.error(f"Error uploading file {local_path} to {destination_blob_name}: {str(e)}")


def transfer_weekly_data_to_gcs(local_data_path, gcs_bucket_name, gcs_destination_folder):
    """Transfer locally collected data to Google Cloud Storage."""
    logging.info("Starting weekly data transfer to Google Cloud Storage...")

    local_files = [f for f in os.listdir(local_data_path) if os.path.isfile(os.path.join(local_data_path, f))]

    for local_file in local_files:
        local_file_path = os.path.join(local_data_path, local_file)
        gcs_blob_name = f"{gcs_destination_folder}/{local_file}"

        upload_to_gcs(gcs_bucket_name, local_file_path, gcs_blob_name)

    logging.info("Weekly data transfer to Google Cloud Storage completed.")

if __name__ == "__main__":
    # TODO: Create environment or config for these data
    local_data_path = "/app/result/weekly/data_collection"
    # /app/data/weekly/upload/
    # local_data_path = "C:/Users/harit/Documents/Visual Studio 2022/MLDockerTest/ML_DCASE2023Task2DataSet/result/weekly/data_collection"
    gcs_bucket_name = "dcase2023bucketdataset"
    gcs_destination_folder = "DcaseDevDataSetResult"

    transfer_weekly_data_to_gcs(local_data_path, gcs_bucket_name, gcs_destination_folder)
