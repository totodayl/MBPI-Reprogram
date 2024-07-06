import datetime
import pandas as pd
import psycopg2
from datetime import timedelta


conn = psycopg2.connect(
    host="192.168.1.13",
    port=5432,
    dbname='postgres',
    user='postgres',
    password='mbpi'

)
cursor = conn.cursor()

cursor.execute("""
SELECT ((SELECT count(*) FROM qc_num_days
WHERE status = 'Failed' AND qc_type = 'NEW' AND product_code = 'DA5176E')::FLOAT
/ (SELECT COUNT(*) FROM qc_num_days
WHERE product_code = 'DA5176E' AND qc_type = 'NEW')::FLOAT)

""")

result = cursor.fetchall()

print(result)