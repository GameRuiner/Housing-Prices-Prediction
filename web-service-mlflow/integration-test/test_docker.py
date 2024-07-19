import json

import requests
from deepdiff import DeepDiff

with open("house.json", "rt", encoding="utf-8") as f_in:
    house = json.load(f_in)


url = "http://localhost:9696/predict"
actual_response = requests.post(url, json=house, timeout=60).json()
print("actual response:")

print(json.dumps(actual_response, indent=2))

expected_response = {"model_name": "pipeline-random-forest-reg-model", "sale_price": 319584.46}

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff={diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff
