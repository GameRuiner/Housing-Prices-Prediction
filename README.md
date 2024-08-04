# Housing Prices Prediction Project

## Project Overview

This project is based on the Kaggle competition "Housing Prices Competition" which aims to predict the final prices of residential homes in Ames, Iowa. The dataset contains 79 explanatory variables that describe almost every aspect of the homes, from the number of bedrooms to the year built.

## Problem Description

In the real estate market, accurately predicting the selling price of a house is crucial for buyers, sellers, and investors. House prices are influenced by various factors including location, size, condition, and other property characteristics. The challenge is to develop a model that can predict the sale prices of houses given these features.

## Problem Statement

The primary problem this project addresses is the need for an accurate predictive model for house prices. By leveraging the dataset provided in the Kaggle competition, we aim to build a machine learning model that can predict the sale price of a house based on its features. This model can be useful for:

* **Homebuyers** who want to assess whether a house is fairly priced.
* **Sellers** who need to set a competitive and realistic selling price.
* **Real estate agents** who provide pricing advice to their clients.
* **Investors** who are evaluating the potential return on investment for different properties.


## Project Goals

* **Data Exploration and Preprocessing:** Understand the dataset, handle missing values, and preprocess the data for modeling.
* **Feature Engineering:** Extract meaningful features and create new ones that can help improve the model's performance.
* **Model Building:** Develop and train various machine learning models to predict house prices.
* **Model Evaluation:** Evaluate the models using appropriate metrics and select the best-performing one.
* **Prediction:** Use the selected model to make predictions on unseen data.


## Dataset

The dataset used in this project includes 79 features such as:

* **Lot Area:** Lot size in square feet.
* **Overall Qual:** Overall material and finish quality.
* **Year Built:** Original construction date.
* **Gr Liv Area:** Above grade (ground) living area square feet.
* **Full Bath:** Full bathrooms above grade.

And many more features that describe the physical attributes and conditions of the homes.

## How to run

The project includes testing, quality checks, building Docker containers, and running integration tests.

### Prerequisites

Before you begin, ensure you have the following installed:

* Docker
* Docker Compose
* Python (with pip and virtualenv)
* Pre-commit
* Pytest
* Linter tools: isort, black, pylint

### Step-by-Step Instructions

1. **Clone the Repository**

   Clone the project repository to your local machine.
   ```sh
   git clone https://github.com/GameRuiner/Housing-Prices-Prediction
   cd Housing-Prices-Prediction
   ```
2. **Set Up the Environment**
   
    Create a Python virtual environment and activate it.
     ```sh
    python3 -m venv venv
    source venv/bin/activate
     ```
   Install the pre-commit hooks.
   ```sh
   make setup
   ```
3. **Run Quality Checks**

   Ensure the code meets quality standards by running the following command:
   ```sh
   make quality_checks
   ```
   This command runs isort, black, and pylint to check and format the code.
   
4. **Run Tests**

   Execute the tests to verify the functionality of the code.
   ```sh
   make test
   ```
   This command runs the tests located in ./web-service-mlflow/tests/ using pytest.

5. **Build the Docker Image**

   Build the Docker image and bring up the services using Docker Compose.
   ```sh
   make build
   ```
   This command will perform quality checks and tests before building the Docker container and starting the services.

6. **Run Integration Tests**

   Execute the integration tests to ensure the Dockerized services work as expected.
   ```sh
   make integration_test
   ```
   This command sets the LOCAL_IMAGE_NAME environment variable and runs the integration tests using a script.




## Conclusion
This project provides a comprehensive solution to the problem of predicting house prices using a rich set of features from the Ames, Iowa housing dataset. By following a structured approach of data exploration, feature engineering, model building, and evaluation, we aim to develop a robust predictive model that can assist various stakeholders in making informed decisions in the real estate market.

Project created for MLOps Zoomcamp
