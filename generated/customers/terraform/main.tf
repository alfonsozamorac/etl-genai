terraform {
  required_version = ">= 0.15"
  required_providers {
    google = "~> 5.0"
  }
}

resource "google_storage_bucket" "temporary_files" {
  project       = "my-cloud-project"
  name          = "temporary-files-dataproc"
  location      = "europe-southwest1"
  force_destroy = true
}

resource "google_storage_bucket" "sales_etl_bucket" {
  project       = "my-cloud-project"
  name          = "sales-etl-bucket"
  location      = "europe-southwest1"
  force_destroy = true
}

resource "google_storage_bucket_object" "sales_folder" {
  name    = "input/sales/"
  bucket  = google_storage_bucket.sales_etl_bucket.name
  content = " "
}

resource "google_storage_bucket_object" "customers_folder" {
  name    = "input/customers/"
  bucket  = google_storage_bucket.sales_etl_bucket.name
  content = " "
}

resource "google_bigquery_dataset" "raw_sales_data" {
  project       = "my-cloud-project"
  dataset_id    = "raw_sales_data"
  friendly_name = "Raw Sales Data"
  description   = "This dataset contains the raw sales data."
  location      = "europe-southwest1"
}

resource "google_bigquery_table" "customer_table" {
  project              = "my-cloud-project"
  dataset_id           = google_bigquery_dataset.raw_sales_data.dataset_id
  deletion_protection  = false
  table_id             = "customer_table"
  schema               = <<EOF
[
  {
    "name": "customer_id",
    "type": "INT64",
    "mode": "REQUIRED",
    "description": "The unique identifier for the customer."
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The name of the customer."
  },
  {
    "name": "email",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The email address of the customer."
  }
]
EOF
}

resource "google_bigquery_table" "sales_table" {
  project              = "my-cloud-project"
  dataset_id           = google_bigquery_dataset.raw_sales_data.dataset_id
  deletion_protection  = false
  table_id             = "sales_table"
  schema               = <<EOF
[
  {
    "name": "order_id",
    "type": "INT64",
    "mode": "REQUIRED",
    "description": "The unique identifier for the order."
  },
  {
    "name": "product",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The product that was purchased."
  },
  {
    "name": "price",
    "type": "FLOAT64",
    "mode": "NULLABLE",
    "description": "The price of the product."
  },
  {
    "name": "amount",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "The quantity of the product that was purchased."
  },
  {
    "name": "customer_id",
    "type": "INT64",
    "mode": "REQUIRED",
    "description": "The unique identifier for the customer who purchased the product."
  }
]
EOF
}

resource "google_bigquery_dataset" "master_sales_data" {
  project       = "my-cloud-project"
  dataset_id    = "master_sales_data"
  friendly_name = "Master Sales Data"
  description   = "This dataset contains the master sales data."
  location      = "europe-southwest1"
}

resource "google_bigquery_table" "bigtable_info" {
  project              = "my-cloud-project"
  dataset_id           = google_bigquery_dataset.master_sales_data.dataset_id
  deletion_protection  = false
  table_id             = "bigtable_info"
  schema               = <<EOF
[
  {
    "name": "customer_id",
    "type": "INT64",
    "mode": "REQUIRED",
    "description": "The unique identifier for the customer."
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The name of the customer."
  },
  {
    "name": "email",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The email address of the customer."
  },
  {
    "name": "order_id",
    "type": "INT64",
    "mode": "REQUIRED",
    "description": "The unique identifier for the order."
  },
  {
    "name": "product",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The product that was purchased."
  },
  {
    "name": "price",
    "type": "FLOAT64",
    "mode": "NULLABLE",
    "description": "The price of the product."
  },
  {
    "name": "amount",
    "type": "INT64",
    "mode": "NULLABLE",
    "description": "The quantity of the product that was purchased."
  }
]
EOF
}