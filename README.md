# DCASE2023DataAnomalyDetection

## Overview

Develop an end-to-end Machine Learning pipeline within Dockerized services that simulate weekly sensor data collection and data upload to Google Cloud, model training, and local inference for anomaly detection.

## Data Collection

1. **Data Retrieval from Google Cloud:**
   - The project assumes the presence of the DCASE standard dataset in a secured server, currently assumed to be hosted on Google Cloud.

2. **Random Audio File Selection:**
   - Random audio files are selected from the DCASE standard dataset for further processing. This step simulates the weekly sensor data collection process.

3. **Metadata Generation:**
   - Metadata is generated for each selected audio file. This metadata includes relevant information about the audio, and it is stored locally.

4. **Local Storage:**
   - Both the selected audio files and their corresponding metadata are stored locally. This local storage serves as a temporary repository for the collected data.

## Data Transfer

1. **Reading Data from Docker Volume:**
   - The locally stored audio files and metadata are read from the Docker volume. The Docker volume acts as a shared storage space between the Data Collection and Data Transfer modules.

2. **Google Cloud Upload:**
   - The collected data, including audio files and metadata, is transferred from the Docker volume to Google Cloud. This step involves pushing the data to a designated location in Google Cloud Storage.

3. **Purpose of Data Transfer:**
   - The transferred data on Google Cloud can be utilized for subsequent stages of the project, such as model training and evaluation. This forms the initial stage of building an end-to-end machine learning pipeline for anomaly detection.

These steps summarize the sample project's current focus on the Data Collection and Data Transfer modules, laying the foundation for further stages in the machine learning pipeline.

## Requirements

- Python 3.8
- pandas==1.3.3
- google-cloud-storage==1.44.0
- requirements.txt

## Setup

**Clone the repository:**
- [git clone https://github.com/your-username/your-repository.git](https://github.com/MinchalaVenkatSunil/ML_DCASE2023Task2DataSet.git)

**Set up your Python environment**
- Provide your on-push branch trigger in the 'ci.cd.yml' pipeline

**Google Cloud Authentication**
- Obtain a service account key (JSON file) and save it as 'mldocker-key-gcp.json' in the project root

**Google cloud storage Bucket**
- Create a bucket named 'dcase2023bucketdataset' and transfer the data set with a similar DCASEDataSet format like test, train, attributes_00.csv, etc. As we move on, we will collect the data from the source directly, and the next steps will continue. 

- /dev_data  
    - /raw
        - /fan
            - /train (only normal clips)  
                - /section_00_source_train_normal_0000_<attribute>.wav  
            - /test 
                - /section_00_source_test_normal_0000_<attribute>.wav  
            - attributes_00.csv (attribute csv for section 00)
    - /gearbox (The other machine types have the same directory structure as fan.)  
    - /bearing
    - /slider (`slider` means "slide rail")
    - /ToyCar  
    - /ToyTrain  
    - /valve   

**Add your secrets**
- https://github.com/MinchalaVenkatSunil/ML_DCASE2023Task2DataSet/settings/secrets/actions
- Provide the below secrets under the above link.
- ![image](https://github.com/MinchalaVenkatSunil/ML_DCASE2023Task2DataSet/assets/137503198/5e95edfc-34c7-47f9-a2e6-583940089ecc)

**Additionally**
- Docker Desktop
- Google Cloud SDK shell
- VS code with necessary extensions related to Git, Docker, git lens, Gihub actions, etc.

## Components

### Data Collection Simulation Service
- Docker Repository: `ml-data-collection-service`
- Python script: `data_collection_simulation.py`

### Data Transfer to Google Cloud Service
- Docker container: `ml-data-transfer-service`
- Python script: `data_transfer_to_gcs.py`

### Model Training on Google Cloud Service
- Docker container: `ml-model-training-service`
- Python script: `model_training_on_gcp.py`

### Model Evaluation and Update Service
- Docker container: `ml-model-evaluation-and-update-service`
- Python script: `model_evaluation_and_update.py`

### CI/CD Pipeline
- GitHub Actions workflow: `.github/workflows/ci-cd.yml`

## Usage
- Check the CI/CD pipeline for automated builds and deployments on branch push changes.

## Additional info

## Data Collection Feature Update

- Improved logic to collect metadata along with selected audio files.
- Metadata collected in JSON format.
- Simulated weekly data collection, selecting random test and train data from the development set.

## Data Transfer

- Transferred locally collected data to Google Cloud Storage.
- Collected metadata along with audio files.

## Docker File

- Added volume for storing large data.
- Copied respective files to respective folders in the local system for easy viewing.
- Added cron jobs for specific weekdays.
- Initiated cron jobs for data transfer, with future plans to use serverless functions for weekly script triggers within Docker containers.
- Established pipelines comprising jobs for Docker image processes such as building, tagging, and pushing.
- Configured jobs to build Docker files, execute the data collection job, and run the data transfer job using Docker images.
- Initially attempted to use `docker/build-push-action@v5` but encountered issues, so the action was reverted.

## Overall Requirement Base Code

- Cleaned up and refactored.
- Added locally tested results to `.gitignore`.
- Updated and organized files for maintainability. A couple of files clean up is needed after temporary testing.
- Introduced a CI/CD pipeline using GitHub Actions.
- Implemented services for data collection simulation and data transfer to Google Cloud.
- Enhanced simulation scripts for weekly data collection.

## Pending Tasks/TODOs

- Create an environment or config for data.
- Move logging level config.
- Improvise logic in certain areas.
- Transition to serverless functions for automated weekly script triggers.
- Address any outstanding issues with `docker/build-push-action`.
- Additional improvements and optimizations as needed.
