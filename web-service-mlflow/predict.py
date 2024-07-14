import os
import mlflow
from flask import Flask, request, jsonify
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service-account.json'
MLFLOW_TRACKING_URI = 'http://tracking:5000' 
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

model_name = "pipeline-random-forest-reg-model"
model_version = 2

model_uri = f"models:/{model_name}/{model_version}"
model = mlflow.sklearn.load_model(model_uri)

def prepare_features(data):
  features = pd.DataFrame([data]).select_dtypes(exclude=['object'])
  return features


def predict(features):
  preds = model.predict(features)
  return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    house = request.get_json()
    features = prepare_features(house)
    pred = predict(features)
    result = {
        'sale_price': pred,
        'model_name': model_name
    }
    return jsonify(result)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=9696)
  
  
