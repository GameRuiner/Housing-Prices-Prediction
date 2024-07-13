# from airflow import DAG
# from airflow.operators.python import PythonOperator
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def load_data():
  # Read the data
  X_full = pd.read_csv('/opt/airflow/input/train.csv', index_col='Id')
  X_test_full = pd.read_csv('/opt/airflow/input/test.csv', index_col='Id')
  
  # Remove rows with missing target, separate target from predictors
  X_full.dropna(axis=0, subset=['SalePrice'], inplace=True)
  y = X_full.SalePrice 
  X_full.drop(['SalePrice'], axis=1, inplace=True)
  
  # To keep things simple, we'll use only numerical predictors
  X = X_full.select_dtypes(exclude=['object'])
  X_test = X_test_full.select_dtypes(exclude=['object'])
  
  df = pd.concat([X, y], axis=1)
  df.to_csv('/tmp/train.csv', index=False)
  X_test.to_csv('/tmp/test.csv', index=False)
  
  # Break off validation set from training data
  # X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
  #                                                     random_state=0)
  

# def train_random_forest():
#     data = pd.read_csv('/tmp/data.csv')
#     X = data.drop(columns=['species'])
#     y = data['species']
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     return train_model('random_forest', RandomForestRegressor, X_train, y_train, X_test, y_test)