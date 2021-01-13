import psycopg2
import pandas as pd

CONNECTION = "postgres://admin:carbonara@localhost:5432/sales"
conn = psycopg2.connect("dbname=sales user=postgres")
cur = conn.cursor()
#cur.execute("""SELECT * FROM am_data""")
def create_panads_table(sql_query,database = conn):
    table = pd.read_sql_query(sql_query,database)
    return table

df = create_panads_table("SELECT * FROM am_data")
print(df.shape)