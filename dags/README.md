# Airflow DAG: Training and Selecting the Best Model

This Airflow DAG trains multiple machine learning models on a housing prices dataset and selects the best model based on the mean absolute error (MAE). The best model is then logged to MLflow.

## Features

* **Data Loading**: Loads training and validation data from CSV files.
* **Model Training**: Trains three different models using different imputation strategies.
* **Model Selection**: Evaluates the models and selects the best one based on MAE.
* **MLflow Logging**: Logs the best model and associated metrics to MLflow.

## Prerequisites

Airflow and MLflow containers coming from docker compose.
Ensure you have the Google Cloud Platform (GCP) credentials for accessing Google Cloud Storage.

## DAG Overview

### Tasks

1. **Load Data**
   * Loads the training and validation data from CSV files.
   * Prepares the data by separating the target variable and handling missing values.
  
2. **Train Reduced Model**
   * Trains a RandomForestRegressor on the dataset with columns containing missing values removed.
  
3. **Train Mean Model**
   * Trains a RandomForestRegressor with missing values imputed using the mean strategy.
  
4. **Train Median Model**
   * Trains a RandomForestRegressor with missing values imputed using the median strategy.
  
5. **Select Best Model**
   * Evaluates the trained models on the validation set.
   * Selects the best model based on the mean absolute error.
   * Logs the best model to MLflow.
  
## Usage

### Setting Up the Environment

1. **Clone the Repository**
   
   Clone the project repository to your local machine.
   
   ```sh
   git clone https://github.com/GameRuiner/Housing-Prices-Prediction
   cd Housing-Prices-Prediction/
   ```
2. **Configuring Airflow**
   
   Docker compose will set up everyhing for you.
   
   ```sh
   make build
   ```

3. **Access Airflow UI**
   
   To access airflow web server, use `localhost:8080` URL.

   
