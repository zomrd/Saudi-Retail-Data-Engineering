
import sys
import logging
import pandas as pd
import os
from sqlalchemy import create_engine, text
from getpass import getpass


# =====================================
# 1. LOGGING CONFIGURATION
# =====================================

logging.basicConfig(
    filename="etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


# =====================================
# 2. ERROR HANDLING
# =====================================

def handle_error(error):
    logging.error(
        "ETL Pipeline failed: %s",
        error,
        exc_info=True
    )

    print("\nETL Pipeline failed!")
    print("Error:", error)

    sys.exit(1)


# =====================================
# 3. MAIN ETL PIPELINE
# =====================================

def main():

    logging.info("ETL Pipeline started")

    # =====================================
    # DATABASE CONNECTION
    # =====================================

    username = "postgres"

    password = os.environ.get("POSTGRES_PASSWORD")

    if not password:
        raise RuntimeError(
            "POSTGRES_PASSWORD environment variable is not set"
        )

    engine = create_engine(
        "postgresql+psycopg2://",
        connect_args={
            "host": os.environ.get("POSTGRES_HOST", "172.18.0.1"),
            "port": 5432,
            "dbname": "saudi_retail_dw",
            "user": username,
            "password": password,
        },
    )

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM cleaned_sales")
        )
        count = result.scalar()

    print("Connection successful!")
    print("Total sales rows:", count)

    logging.info("Database connection successful")

    # =====================================
    # EXTRACT
    # =====================================

   
    query = """
    SELECT *
    FROM cleaned_sales
    """

    with engine.connect() as connection:
        df = pd.read_sql_query(text(query), connection)

    print("\nExtract completed!")
    print(df.head())
    print("Total rows:", len(df))
    print("Columns:", df.columns.tolist())

    logging.info(
        "Extract completed | Rows: %s",
        len(df)
    )

    # =====================================
    # TRANSFORM
    # =====================================

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    # Remove duplicate rows
    df = df.drop_duplicates().copy()

    # Convert quantity and price to numeric
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unitprice"] = pd.to_numeric(
        df["unitprice"],
        errors="coerce"
    )

    # Remove missing important values
    df = df.dropna(
        subset=[
            "orderid",
            "productname",
            "quantity",
            "unitprice"
        ]
    ).copy()

    # Remove invalid quantities and prices
    df = df[
        (df["quantity"] > 0) &
        (df["unitprice"] >= 0)
    ].copy()

    # Calculate total sales
    df["totalsales"] = (
        df["quantity"] * df["unitprice"]
    )

    print("\nTransform completed!")
    print("Cleaned rows:", len(df))
    print("Total sales:", df["totalsales"].sum())

    logging.info(
        "Transform completed | Cleaned rows: %s",
        len(df)
    )

    # =====================================
    # DATA QUALITY CHECKS
    # =====================================

    print("\nRunning data quality checks...")

    assert len(df) > 0, "Dataset is empty!"

    assert df["orderid"].isnull().sum() == 0, \
        "Missing Order IDs found!"

    assert (df["quantity"] > 0).all(), \
        "Invalid quantities found!"

    assert (df["unitprice"] >= 0).all(), \
        "Invalid prices found!"

    assert (
        df["totalsales"] ==
        df["quantity"] * df["unitprice"]
    ).all(), "Incorrect total sales found!"

    print("All data quality checks passed!")

    logging.info("Data quality checks passed")

    # =====================================
    # LOAD + CREATE ANALYTICS VIEW
    # =====================================

    table_name = "sales_analytics"

    view_query = """
    CREATE OR REPLACE VIEW product_sales_summary AS
    SELECT
        productname,
        SUM(quantity) AS total_quantity,
        SUM(totalsales) AS total_revenue,
        COUNT(DISTINCT orderid) AS total_orders
    FROM sales_analytics
    GROUP BY productname
    """

    with engine.begin() as connection:

        # Remove old view
        connection.execute(
            text("DROP VIEW IF EXISTS product_sales_summary")
        )

        # Load cleaned data
        df.to_sql(
            name=table_name,
            con=connection,
            if_exists="replace",
            index=False
        )

        # Create analytics view
        connection.execute(text(view_query))

    print("\nLoad completed successfully!")
    print("Table:", table_name)
    print("Rows loaded:", len(df))

    logging.info(
        "Load completed | Rows loaded: %s",
        len(df)
    )

    print("\nProduct sales summary view created!")

    logging.info(
        "Product sales summary view created successfully"
    )

    # =====================================
    # PIPELINE COMPLETED
    # =====================================

    logging.info(
        "ETL Pipeline completed successfully"
    )

    print("\nETL Pipeline completed successfully!")


# =====================================
# 4. RUN PIPELINE
# =====================================

if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        handle_error(error)
