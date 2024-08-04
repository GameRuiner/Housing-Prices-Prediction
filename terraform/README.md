# Terraform Module

This Terraform module sets up the necessary infrastructure on Google Cloud Platform (GCP) to host an MLflow web service. The module provisions a storage bucket for model storage, a virtual private cloud (VPC) network, a subnet, a compute instance to run the Flask application, and firewall rules to allow SSH and HTTP access.

## Features

* **Google Cloud Storage Bucket**: A storage bucket named *mlflow-models-bucket* is created in the *europe-north1* region to store MLflow models.
* **VPC Network and Subnet**: A custom VPC network and subnet are created to host the compute resources.
* **Compute Instance**: A compute instance named *web-service-mlflow* is created with a Debian 11 image, running a startup script to install and set up the necessary Python packages for the Flask application.
* **Firewall Rules**: Firewall rules are set up to allow SSH access on port 22 and HTTP access on port 5000.

## Usage

### Prerequisites

Ensure you have the following:
* A GCP project
* Terraform installed

### Variables

The following variables must be provided:

* *project*: The GCP project ID.
* *region*: The region where resources will be created.

### Initialize and Apply

1. **Initialize the Terraform configuration**:
   
   ```sh
   terraform init
   ```

2. **Apply the Terraform plan**:

   ```sh
   terraform apply
   ```

   Confirm the plan and proceed with the deployment.

### Resources Created

* **Google Storage Bucket**: *mlflow-models-bucket*
* **Google Compute Network**: *my-custom-mode-network*
* **Google Compute Subnetwork**: *my-custom-subnet*
* **Google Compute Instance**: *web-service-mlflow*
* **Google Compute Firewall Rule for SSH**: *allow-ssh*
* **Google Compute Firewall Rule for Flask**: *flask-app-firewall*

## Cleanup

To clean up the resources created by this module, run:

```sh
terraform destroy
```

Confirm the plan and proceed with the destruction of the resources.


