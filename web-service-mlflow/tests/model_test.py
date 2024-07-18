import predict
import pandas as pd

class ModelMock:
  def __init__(self, value):
    self.value = value

  def predict(self, X):
    n = len(X)
    return [self.value] * n

def test_model_uri():
  model_name = 'random_forest'
  model_version = 3
  model_uri = predict.create_model_uri(model_name, model_version)
  assert model_uri ==  f"models:/{model_name}/{model_version}"
  
def test_prepare_features():
  house = {
    "MSSubClass": 20,
    "LotShape": "Reg",
    "LotFrontage": 90.0,
    "LandContour": "Lvl",
    "LotArea": 11694,
    "Utilities": "AllPub"
  }
  features = predict.prepare_features(house)       
  expected = pd.DataFrame([{
    "MSSubClass": 20,
    "LotFrontage": 90.0,
    "LotArea": 11694,
  }])
  assert features.equals(expected)
  
def test_predict():
  model_mock = ModelMock(10.0)
  features = {
    "MSSubClass": 20,
    "LotShape": "Reg",
  }
  actual_prediction = predict.predict(features, model_mock)
  expected_prediction = 10.0
  assert actual_prediction == expected_prediction                                     