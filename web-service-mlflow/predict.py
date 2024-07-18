import os
import mlflow
from flask import Flask, request, jsonify
import pandas as pd
import psycopg
import datetime
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service-account.json'
MLFLOW_TRACKING_URI = 'http://tracking:5000' 
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model_name = "pipeline-random-forest-reg-model"
model_version = 2

model_uri = f"models:/{model_name}/{model_version}"
model = mlflow.sklearn.load_model(model_uri)

create_table_statement = """
create table if not exists metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""

target = "SalePrice"
num_features = ["LotFrontage", "LotArea", "MasVnrArea", "BsmtFinSF1", "BsmtFinSF2", "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "LowQualFinSF", "GrLivArea", "GarageArea", "WoodDeckSF", "OpenPorchSF", "EnclosedPorch", "3SsnPorch", "ScreenPorch", "PoolArea", "MiscVal"]
cat_features = ["MSSubClass", "OverallQual", "OverallCond", "YearBuilt", "YearRemodAdd", "BsmtFullBath", "BsmtHalfBath", "FullBath", "HalfBath", "BedroomAbvGr", "KitchenAbvGr", "TotRmsAbvGrd", "Fireplaces", "GarageYrBlt", "GarageCars", "MoSold", "YrSold"]

column_mapping = ColumnMapping(
    target=None,
    prediction='SalePrice',
    numerical_features=num_features,
    categorical_features=cat_features
)

report = Report(metrics=[
    ColumnDriftMetric(column_name='SalePrice'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric()
])

df_full = pd.read_csv('/tmp/input/train.csv', index_col='Id')
df_full.dropna(axis=0, subset=['SalePrice'], inplace=True)
train_data = df_full.select_dtypes(exclude=['object'])

def prep_db():
	with psycopg.connect(f"host=db port=5432 user={os.environ['POSTGRES_USER']} password={os.environ['POSTGRES_PASSWORD']}", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='evidently_monitoring'")
		if len(res.fetchall()) == 0:
			conn.execute("create database evidently_monitoring;")
		with psycopg.connect(f"host=db port=5432 dbname=evidently_monitoring user={os.environ['POSTGRES_USER']} password={os.environ['POSTGRES_PASSWORD']}") as conn:
			conn.execute(create_table_statement)

def prepare_features(data):
  features = pd.DataFrame([data]).select_dtypes(exclude=['object'])
  return features


def predict(features):
  preds = model.predict(features)
  return float(preds[0])


app = Flask('house-price-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    house = request.get_json()
    features = prepare_features(house)
    pred = predict(features)
    features['SalePrice'] = pred
    report.run(reference_data=train_data, current_data=features, column_mapping=column_mapping)
    report_result = report.as_dict()
    prediction_drift = report_result['metrics'][0]['result']['drift_score']
    num_drifted_columns = report_result['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = report_result['metrics'][2]['result']['current']['share_of_missing_values']
    with psycopg.connect(f"host=db port=5432 dbname=evidently_monitoring user={os.environ['POSTGRES_USER']} password={os.environ['POSTGRES_PASSWORD']}") as conn:
      with conn.cursor() as curr:
        curr.execute(
          "insert into metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
          (datetime.datetime.now(), prediction_drift, num_drifted_columns, share_missing_values)
        )
    result = {
        'sale_price': pred,
        'model_name': model_name
    }
    return jsonify(result)


if __name__ == "__main__":
  prep_db()
  app.run(debug=True, host='0.0.0.0', port=9696)
  
  
