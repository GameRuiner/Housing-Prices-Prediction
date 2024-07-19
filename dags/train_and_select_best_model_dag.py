import os
from datetime import datetime

import joblib
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow import DAG
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import mlflow


def load_data():
    # Read the data
    X_full = pd.read_csv("/opt/airflow/input/train.csv", index_col="Id")
    X_test_full = pd.read_csv("/opt/airflow/input/test.csv", index_col="Id")

    # Remove rows with missing target, separate target from predictors
    X_full.dropna(axis=0, subset=["SalePrice"], inplace=True)
    y = X_full.SalePrice
    X_full.drop(["SalePrice"], axis=1, inplace=True)

    # To keep things simple, we'll use only numerical predictors
    X = X_full.select_dtypes(exclude=["object"])
    X_test = X_test_full.select_dtypes(exclude=["object"])

    # Break off validation set from training data
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
    X_train.to_csv("/tmp/X_train.csv", index=False)
    X_valid.to_csv("/tmp/X_valid.csv", index=False)
    y_train.to_csv("/tmp/y_train.csv", index=False)
    y_valid.to_csv("/tmp/y_valid.csv", index=False)

    df = pd.concat([X, y], axis=1)
    df.to_csv("/tmp/train.csv", index=False)
    X_test.to_csv("/tmp/test.csv", index=False)


def train_reduced_model():
    model_name = "reduced_model"
    X_train = pd.read_csv("/tmp/X_train.csv")
    y_train = pd.read_csv("/tmp/y_train.csv")["SalePrice"]
    X_valid = pd.read_csv("/tmp/X_valid.csv")
    cols_with_missing_values = [col for col in X_train.columns if X_train[col].isnull().any()]
    reduced_X_train = X_train.drop(cols_with_missing_values, axis=1)
    reduced_X_valid = X_valid.drop(cols_with_missing_values, axis=1)
    reduced_X_valid.to_csv(f"/tmp/X_{model_name}_valid.csv", index=False)
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(reduced_X_train, y_train)
    joblib.dump(model, f"/tmp/{model_name}.joblib")


def train_mean_model():
    model_name = "mean_model"
    X_train = pd.read_csv("/tmp/X_train.csv")
    y_train = pd.read_csv("/tmp/y_train.csv")["SalePrice"]
    imputer = SimpleImputer(strategy="mean")
    imputed_X_train = pd.DataFrame(imputer.fit_transform(X_train))
    imputed_X_train.columns = X_train.columns
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    pipeline = Pipeline([("imputer", imputer), ("model", model)])
    model.fit(imputed_X_train, y_train)
    joblib.dump(pipeline, f"/tmp/{model_name}.joblib")


def train_median_model():
    model_name = "median_model"
    X_train = pd.read_csv("/tmp/X_train.csv")
    y_train = pd.read_csv("/tmp/y_train.csv")["SalePrice"]
    imputer = SimpleImputer(strategy="median")
    imputed_X_train = pd.DataFrame(imputer.fit_transform(X_train))
    imputed_X_train.columns = X_train.columns
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    pipeline = Pipeline([("imputer", imputer), ("model", model)])
    model.fit(imputed_X_train, y_train)
    joblib.dump(pipeline, f"/tmp/{model_name}.joblib")


def select_best_model():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/config/silicon-data-423218-q0-179a2dbeb763.json"
    mlflow.set_tracking_uri("http://tracking:5000")
    mlflow.set_experiment("housing-prices-experiment")
    results = []
    for model_name in ["reduced_model", "mean_model", "median_model"]:
        model = joblib.load(f"/tmp/{model_name}.joblib")
        if model_name == "reduced_model":
            X = pd.read_csv(f"/tmp/X_{model_name}_valid.csv")
        else:
            X = pd.read_csv("/tmp/X_valid.csv")
        y = pd.read_csv("/tmp/y_valid.csv")
        with mlflow.start_run():
            mlflow.set_tag("developer", "marko")
            mlflow.log_param("valid-input-shape", X.shape)
            preds = model.predict(X)
            mae = mean_absolute_error(y, preds)
            mlflow.log_metric("mae", mae)
            results.append({"model_name": model_name, "mae": mae, "model": model})
    best_model = min(results, key=lambda x: x["mae"])
    print(f"Best model: {best_model['model_name']} with MAE: {best_model['mae']}")
    mlflow.sklearn.log_model(
        sk_model=best_model["model"],
        artifact_path="pipeline-model",
        registered_model_name="pipeline-random-forest-reg-model",
    )


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
}

with DAG(
    "train_and_select_best_model", default_args=default_args, schedule="@daily", catchup=False, tags=["train"]
) as dag:

    load_data_op = PythonOperator(task_id="load_data", python_callable=load_data)

    train_reduced_model_op = PythonOperator(task_id="train_reduced_model", python_callable=train_reduced_model)

    train_mean_model_op = PythonOperator(task_id="train_mean_model", python_callable=train_mean_model)

    train_median_model_op = PythonOperator(task_id="train_median_model", python_callable=train_median_model)

    select_best_model_op = PythonOperator(task_id="select_best_model", python_callable=select_best_model)

    load_data_op >> [train_reduced_model_op, train_mean_model_op, train_median_model_op] >> select_best_model_op
