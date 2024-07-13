FROM apache/airflow:2.9.2

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install python packages
COPY requirements.txt /tmp

RUN pip install -v -r /tmp/requirements.txt
