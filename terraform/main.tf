provider "google" {
  project = var.project
  region = var.region
}

resource "google_storage_bucket" "model_storage" {
  name     = "mlflow-models-bucket"
  location = "europe-north1"
}

resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "europe-north1"
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_instance" "flask_instance" {
  name         = "web-service-mlflow"
  machine_type = "e2-micro"
  zone         = "europe-central2-a"
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
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
    pip3 install flask google-cloud-storage gunicorn mlflow psycopg2
    EOF
}

resource "google_compute_firewall" "ssh" {
  name = "allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.vpc_network.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "flask" {
  name    = "flask-app-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }
  source_ranges = ["0.0.0.0/0"]
}
