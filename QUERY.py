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
SELECT lot_number FROM quality_control

""")

result = cursor.fetchall()

print(result)