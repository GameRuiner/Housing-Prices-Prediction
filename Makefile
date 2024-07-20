LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=batch-model-price:${LOCAL_TAG}

test:
	pytest ./web-service-mlflow/tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .

build: quality_checks test
	docker-compose up -d

integration_test:
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash ./web-service-mlflow/integraton-test/run.sh

setup:
	pre-commit install
