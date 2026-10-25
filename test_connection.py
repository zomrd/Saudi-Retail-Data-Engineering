
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="saudi_retail_dw",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    ) as conn:
        print("Connected to PostgreSQL successfully!")

        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Orders;")
            count = cursor.fetchone()[0]
            print("Total orders:", count)

except Exception as error:
    print("Connection failed:", error)
