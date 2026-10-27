# Saudi Retail Data Engineering Pipeline

## Project Overview
An end-to-end data engineering project that extracts, cleans, validates, and loads Saudi retail sales data into PostgreSQL, with workflow orchestration using Apache Airflow.

## Tech Stack
- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Apache Airflow
- WSL / Ubuntu

## Pipeline Architecture

Source Data (PostgreSQL)
        |
        v
Python ETL Pipeline
        |
        v
Data Cleaning & Transformation
        |
        v
Data Quality Validation
        |
        v
PostgreSQL Data Warehouse
        |
        v
Sales Analytics & Product Summary View

Apache Airflow orchestrates the ETL pipeline.

## ETL Process

### 1. Extract
Read retail sales records from the PostgreSQL source table `cleaned_sales`.

### 2. Transform
- Remove duplicate records
- Handle missing values
- Convert numeric columns
- Filter invalid sales records
- Calculate total sales

### 3. Validate
Perform data quality checks before loading.

### 4. Load
Load cleaned data into the `sales_analytics` table and create the `product_sales_summary` SQL view.

## Workflow Orchestration
Apache Airflow runs the `saudi_retail_etl` DAG, containing the `run_etl` task.

The DAG is configured with a daily cron schedule:

`0 9 * * *`

The schedule uses the Airflow environment's configured timezone.

## Test Results
- Source records extracted: 8
- Records loaded: 8
- Total sales: 10,435
- Data quality checks: Passed
- Manual ETL execution: Successful
- Airflow DAG execution: Successful

## Project Structure
- `etl_pipeline.py` - Main ETL pipeline
- `dags/saudi_retail_etl_dag.py` - Airflow DAG
- `extract_data.py` - Data extraction script
- `test_connection.py` - PostgreSQL connection test
- `.gitignore` - Excluded local and sensitive files

## Security
Database credentials are provided through environment variables and are not included in the repository.

## Future Improvements
- Add automated data quality reporting
- Add incremental data loading
- Expand the dataset
- Deploy Airflow in a production-ready environment




## Power BI Sales Dashboard

![Saudi Retail Sales Dashboard](Power%20bi/Saudi_Retail_Dashboard.png)
