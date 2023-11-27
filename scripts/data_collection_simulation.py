import logging
from google.cloud import storage
import os
import random
from datetime import datetime, timedelta

# TODO: Move the logging config from here
logging.basicConfig(
    filename='data_collection_simulation.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

def download_file(
        bucket_name, 
        source_blob_name, 
        destination_file_name
        ):
    """Downloads a file from Google Cloud Storage."""
    try:
        json_key_path = "/app/mldocker-4713e7f8b358.json"
        storage_client = storage.Client.from_service_account_json(json_key_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        logging.info(f"Downloaded file: {source_blob_name} to {destination_file_name}")
    except Exception as e:
        logging.error(f"Error downloading file {source_blob_name}: {str(e)}")

def list_files(bucket_name, prefix):
    """Lists all files in a GCS bucket with the given prefix."""
    try:
        json_key_path = "/app/mldocker-4713e7f8b358.json"
        storage_client = storage.Client.from_service_account_json(json_key_path)
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
        file_names = [blob.name for blob in blobs]
        logging.info(f"Listed files in {prefix}: {file_names}")
        return file_names
    except Exception as e:
        logging.error(f"Error listing files in {prefix}: {str(e)}")
        return []

def simulate_weekly_data_collection(
        bucket_name, 
        dataset_folder, 
        output_path
        ):
    logging.info("Starting weekly data collection simulation...")

    os.makedirs(output_path, exist_ok=True)

    # List all machine types in the dataset
    machine_types = list_files(bucket_name, f"{dataset_folder}/")
    machine_types = list(set(machine_types))

    logging.info(f"Machine types: {machine_types}")
    machine_types = [machine_type.split('/')[1] for machine_type in machine_types if '/' in machine_type]
    machine_types = list(set(machine_types))

    logging.info(f"Machine types with split: {machine_types}")

    # Simulate weekly data collection for each machine type
    for machine_type in machine_types:
        machine_type_prefix = f"{dataset_folder}/{machine_type}"

        logging.info(f"Machine type prefix: {machine_type_prefix}")

        sections = list_files(bucket_name, f"{machine_type_prefix}/")
        sections = list(set(sections))
        sections = [section.split('/')[2] for section in sections if '/' in section]
        sections = list(set(sections))

        for section in sections:
            section_prefix = f"{machine_type_prefix}/{section}"

            files = list_files(bucket_name, f"{section_prefix}/")
            files = list(set(files))
            files = [file.split('/')[-1] for file in files if '/' in file and file.endswith('.wav')]
            files = list(set(files))

            # Simulate weekly data collection by randomly selecting a subset of files
            random.shuffle(files)
            weekly_subset = files[:2] # TODO: Move this adjusting number out

            for file_name in weekly_subset:
                source_blob_name = f"{section_prefix}/{file_name}"
                destination_path = os.path.join(output_path, f'{machine_type}_{section}_{file_name}')

                # print(f"Downloading file: {source_blob_name} -> {destination_path}")
                download_file(bucket_name, source_blob_name, destination_path)

    logging.info("Weekly data collection simulation completed.")

if __name__ == "__main__":
    # TODO: Create environment or config for these data
    gcs_bucket_name = "dcase2023bucketdataset"
    gcs_dataset_folder = "DcaseDevDataSet"
    output_path = "result/weekly/data_collection"

    simulate_weekly_data_collection(gcs_bucket_name, gcs_dataset_folder, output_path)
