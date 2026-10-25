
import os
import pandas as pd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv

load_dotenv()

# Database connection
db_url = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=5432,
    database="saudi_retail_dw"
)

engine = create_engine(db_url)

# Extract sales data
query = """
SELECT
    o.OrderID,
    o.OrderDate,
    b.BranchName,
    p.ProductName,
    oi.Quantity,
    oi.UnitPrice,
    oi.Quantity * oi.UnitPrice AS TotalSales
FROM Orders o
JOIN Branches b
    ON o.BranchID = b.BranchID
JOIN OrderItems oi
    ON o.OrderID = oi.OrderID
JOIN Products p
    ON oi.ProductID = p.ProductID
"""

with engine.connect() as connection:
    df = pd.read_sql(query, connection)

print(df)
print("Total rows:", len(df))







# Transform data

# Remove duplicate order items
df = df.drop_duplicates()

# Remove rows with missing important values
df = df.dropna(
    subset=["orderid", "productname", "quantity", "unitprice"]
)

# Convert columns to numeric
df["quantity"] = pd.to_numeric(df["quantity"])
df["unitprice"] = pd.to_numeric(df["unitprice"])

# Remove invalid values
df = df[
    (df["quantity"] > 0) &
    (df["unitprice"] >= 0)
].copy()

# Calculate total sales
df["totalsales"] = df["quantity"] * df["unitprice"]

# Show cleaned data
print("\nCleaned Data:")
print(df)

print("\nTotal Sales:", df["totalsales"].sum())






# Load cleaned data into PostgreSQL

df.to_sql(
    name="cleaned_sales",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully!")
print("Rows loaded:", len(df))
