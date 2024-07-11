FROM python:3.9.19-bullseye

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

COPY [ "predict.py", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]