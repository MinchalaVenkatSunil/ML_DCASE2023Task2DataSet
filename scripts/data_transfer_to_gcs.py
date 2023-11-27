import os
from google.cloud import storage

def upload_to_gcs(local_file_path, bucket_name, destination_blob_name, key_path):
    """Upload a file to Google Cloud Storage."""
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    print(f"Uploaded: {local_file_path} to {destination_blob_name}")

def transfer_data_to_gcs(local_data_folder, bucket_name, key_path):
    """Transfer locally collected data to Google Cloud Storage."""
    print(f"Starting data transfer from {local_data_folder} to {bucket_name}...")

    # Check if the specified path exists
    if os.path.exists(local_data_folder):
        print(f"Contents of the '{local_data_folder}' folder:")
        
        # Get the list of files and directories
        contents = os.listdir(local_data_folder)
        
        # Print each item in the list
        for item in contents:
            print(item)
    else:
        print(f"The folder '{local_data_folder}' does not exist.")

        # Get the list of files and directories
        contents = os.listdir(os.getcwd())
        
        # Print each item in the list
        for item in contents:
            print("Items: {item}")

    for root, dirs, files in os.walk(local_data_folder):
        for file in files:
            local_file_path = os.path.join(root, file)

            # destination_blob_name = os.path.relpath(local_file_path, local_data_folder)
            print(f"\nProcessing: {local_file_path}")
            # upload_to_gcs(local_file_path, bucket_name, destination_blob_name, key_path)

            # Get the relative path without the starting 'local_data_folder'
            relative_path = os.path.relpath(local_file_path, local_data_folder)

            # Combine with the desired prefix and replace os.sep with '/'
            destination_blob_name = f"weekly/upload/{relative_path.replace(os.sep, '/')}"

            # Upload the file to Google Cloud Storage
            upload_to_gcs(local_file_path, bucket_name, destination_blob_name, key_path)

    print("Data transfer completed.")

if __name__ == "__main__":
    print("Starting main...")
    
    # Set configuration details
    local_data_folder = "/app/data/weekly/upload/"  # Adjust to the actual local data folder
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "dcase2023bucketdataset")
    key_path = os.environ.get("GCS_KEY_PATH", "/app/mldocker-4713e7f8b358.json")

    # Transfer data to Google Cloud Storage
    transfer_data_to_gcs(local_data_folder, bucket_name, key_path)

