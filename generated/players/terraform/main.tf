terraform {
  required_version = ">= 0.15"
  required_providers {
    google = "~> 5.0"
  }
}

resource "google_storage_bucket" "temporary_files" {
  project       = "my-cloud-project"
  name          = "temporary-files-dataproc"
  location      = "europe-west1"
  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  project       = "my-cloud-project"
  dataset_id    = "myligue"
  friendly_name = "myligue"
  description   = "myligue"
  location      = "europe-west1"
}

resource "google_bigquery_table" "table" {
  project              = "my-cloud-project"
  dataset_id           = google_bigquery_dataset.dataset.dataset_id
  deletion_protection  = false
  table_id             = "players_goals"
  schema               = <<EOF
[
  {
    "name": "player",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The player"
  },
  {
    "name": "team",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The team"
  },
  {
    "name": "goal_date",
    "type": "DATE",
    "mode": "NULLABLE",
    "description": "The goal date"
  },
  {
    "name": "minute",
    "type": "INTEGER",
    "mode": "NULLABLE",
    "description": "The minute"
  }
]
EOF
}

resource "google_bigquery_table" "table2" {
  project              = "my-cloud-project"
  dataset_id           = google_bigquery_dataset.dataset.dataset_id
  deletion_protection  = false
  table_id             = "players_ranking"
  schema               = <<EOF
[
  {
    "name": "player",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The player"
  },
  {
    "name": "goals_scored",
    "type": "INTEGER",
    "mode": "NULLABLE",
    "description": "The goals scored"
  }
]
EOF
}