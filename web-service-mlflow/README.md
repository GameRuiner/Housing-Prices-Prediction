# Web Service for Housing Price Prediction with MLflow

This web service is designed to predict housing prices using a machine learning model served via MLflow. The service processes input data, makes predictions, and monitors the model's performance by tracking metrics such as prediction drift, the number of drifted columns, and the share of missing values. These metrics are stored in a PostgreSQL database for further analysis.

## Features

* **Prediction Endpoint**: Receives input data, processes it, and returns the predicted house price.
* **Model Integration**: Utilizes MLflow to load and serve the machine learning model.
* **Drift Monitoring**: Calculates and stores metrics related to prediction drift and data quality in a PostgreSQL database.
* **Database Preparation**: Initializes the database and creates necessary tables for storing metrics.

## Key Components

* **Flask Application**: Handles HTTP requests and responses.
* **MLflow**: Loads the pre-trained machine learning model.
* **PostgreSQL**: Stores metrics for monitoring the model's performance.
* **Pandas**: Processes input data to prepare features for prediction.
* **Evidently**: Generates reports on data and model performance to detect drift and other issues.

## Usage

The service exposes an endpoint /predict where you can send JSON data of house features and receive a predicted sale price in response. Additionally, the service monitors and logs various metrics to help you maintain and improve the model's performance over time.
