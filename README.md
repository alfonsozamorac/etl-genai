# PySpark ETL and Infrastructure as Code (IaC) with Vertex AI on GCP

## Documentation

* [Dataproc](https://cloud.google.com/dataproc/docs)
* [Cloud Storage](https://cloud.google.com/storage/docs)
* [BigQuery](https://cloud.google.com/bigquery/docs)
* [VertexAI](https://cloud.google.com/vertex-ai/docs)


## Overview

This Python application use the Vertex AI library on Google Cloud Platform (GCP) for generating Terraform code to deploy infrastructure and pyspark code to extract, transform and load information with natural language.

## Features

- **BigQuery and Cloud Storage:** They will be the data storage.
- **Dataproc:** We will use Dataproc Batches to execute the generated pyspark code to process the information.
- **Vertex AI Integration:** Leverage the Vertex AI library from Google Cloud Platform to generate Terraform code for infrastructure deployment and ETL the information.
- **Terraform:** We will use code in HCL to automate the creation and destruction of infrastructure.

## Prerequisites

- Python >= 3.5
- GCP Account with Vertex AI API access
- Google Cloud SDK installed and configured
- Terraform installed

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/alfonsozamorac/etl-genai.git
   cd etl-genai
   ```

2. Creation of Virtual Env:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install GCP library:

   ```bash
   pip3 install --upgrade google-cloud-aiplatform
   ```

4. Export your GCP credentials:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="your_credentials_file.json"
   ```

5. You can export your GCP project to generate the request automatically:

   ```bash
   export MY_GCP_PROJECT="your_project_name"
   ```

## Usage example players


1. Execute py program to generate the hcl and pyspark code for players example:

   ```bash
   python3 ai_gen.py players ${MY_GCP_PROJECT}
   ```

2. Create infraestructure with terraform:

   ```bash
   terraform -chdir="generated/players/terraform" init
   terraform -chdir="generated/players/terraform" apply --auto-approve
   ```

3. Insert data into Bigquery table:

   ```bash
   bq query --project_id=${MY_GCP_PROJECT} --use_legacy_sql=False < example_data/players/insert_players_example.sql
   ```

4. Create a Batch in Dataproc with pyspark code:

   ```bash
   gcloud dataproc batches submit pyspark generated/players/python/etl.py --version=1.1 --batch=players-genai-$RANDOM --region="europe-west1" --deps-bucket=gs://temporary-files-dataproc --project=${MY_GCP_PROJECT} --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar  
   ```

5. Go to GCP UI and see the results, or execute the below query to get them:

   ```bash
   bq query --project_id=${MY_GCP_PROJECT} --use_legacy_sql=False "SELECT * FROM myligue.players_ranking"
   ```

6. Destroy infraestructure:

   ```bash
   terraform -chdir="generated/players/terraform" destroy --auto-approve
   ```

## Usage example customers

1. Execute py program to generate the hcl and pyspark code for customers example:

   ```bash
   python3 ai_gen.py customers ${MY_GCP_PROJECT}
   ```

2. Create infraestructure with terraform:

   ```bash
   terraform -chdir="generated/customers/terraform" init
   terraform -chdir="generated/customers/terraform" apply --auto-approve
   ```

3. Insert data into Cloud Storage folders:

   ```bash
   gcloud storage cp example_data/customers/sales.csv gs://sales-etl-bucket/input/sales
   gcloud storage cp example_data/customers/customers.csv gs://sales-etl-bucket/input/customers
   ```

4. Create a Batch in Dataproc with pyspark code.

   ```bash
   gcloud dataproc batches submit pyspark generated/customers/python/etl.py --version=1.1 --batch=customers-genai-$RANDOM --region="europe-west1" --deps-bucket=gs://temporary-files-dataproc --project=${MY_GCP_PROJECT} --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar  
   ```

5. Go to GCP UI and see the results, or execute the below query to get them:

   ```bash
   bq query --project_id=${MY_GCP_PROJECT} --use_legacy_sql=False "SELECT * FROM raw_sales_data.customer_table"
   bq query --project_id=${MY_GCP_PROJECT} --use_legacy_sql=False "SELECT * FROM raw_sales_data.sales_table"
   bq query --project_id=${MY_GCP_PROJECT} --use_legacy_sql=False "SELECT * FROM master_sales_data.bigtable_info"
   ```

6. Destroy infraestructure:

   ```bash
   terraform -chdir="generated/customers/terraform" destroy --auto-approve
   ```

## Usage create new example

1. Insert a new K,V element in 'examples' dictionary variable in ai_gen.py.

2. Execute py program to generate the hcl and pyspark code for your example:

   ```bash
   python3 ai_gen.py ${your_example_name} ${MY_GCP_PROJECT}
   ```

2. Create infraestructure with terraform:

   ```bash
   terraform -chdir="generated/${your_example_name}/terraform" init
   terraform -chdir="generated/${your_example_name}/terraform" apply --auto-approve
   ```

3. Insert data into Cloud Storage or Bigquery

5. Create a Batch in Dataproc with pyspark code.

   ```bash
   gcloud dataproc batches submit pyspark generated/customers/python/etl.py --version=1.1 --batch=${your_example_name}-genai-$RANDOM --region="europe-west1" --deps-bucket=gs://temporary-files-dataproc --project=${MY_GCP_PROJECT} --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar  
   ```

6. Check results into Cloud Storage or Bigquery

7. Destroy infraestructure:

   ```bash
   terraform -chdir="generated/${your_example_name}/terraform" destroy --auto-approve
   ```