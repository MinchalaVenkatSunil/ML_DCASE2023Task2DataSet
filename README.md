# Anomaly Detection Pipeline

## Components

### Data Collection Simulation Service
- Docker container: `data_collection_simulation`
- Python script: `data_collection_simulation.py`

### Data Transfer to Google Cloud Service
- Docker container: `data_transfer_to_gcs`
- Python script: `data_transfer_to_gcs.py`

### Model Training on Google Cloud Service
- Docker container: `model_training_on_gcp`
- Python script: `model_training_on_gcp.py`

### Model Evaluation and Update Service
- Docker container: `model_evaluation_and_update`
- Python script: `model_evaluation_and_update.py`

### CI/CD Pipeline
- GitHub Actions workflow: `.github/workflows/ci-cd.yml`

## Usage

- Follow the steps in the README to set up and run each service.
- Check the CI/CD pipeline for automated builds and deployments.
