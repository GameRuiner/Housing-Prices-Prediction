provider "google" {
  credentials = file("../web-service-mlflow/config/silicon-data-423218-q0-179a2dbeb763.json")
  project     = "silicon-data-423218-q0"
  region      = "europe-north1"
}

resource "google_storage_bucket" "model_storage" {
  name     = "mlflow-models-marko"
  location = "europe-north1"
}

resource "google_compute_instance" "flask_instance" {
  name         = "web-service-mlflow"
  machine_type = "n1-standard-1"
  zone         = "europe-central2-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"

    access_config {
    }
  }

  metadata_startup_script = <<-EOF
    #! /bin/bash
    sudo apt-get update
    sudo apt-get install -y python3-pip
    pip3 install flask google-cloud-storage
    # Add commands to deploy your Flask app
    EOF
}
