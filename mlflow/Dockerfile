FROM python:3.9.19-bullseye

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install python packages
COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

# Clean up to reduce image size
RUN rm -rf /tmp/requirements.txt