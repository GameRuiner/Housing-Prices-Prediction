FROM python:3.9.19-bullseye

# Upgrade pip to the latest version
RUN pip install --upgrade pip

WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

COPY requirements.txt ./

# Install python packages
RUN pip install -v -r /app/requirements.txt

COPY predict.py ./

COPY ["./config/silicon-data-423218-q0-179a2dbeb763.json", "./service-account.json"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]