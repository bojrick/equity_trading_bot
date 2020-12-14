import psycopg

# Connect to your postgres DB
CONNECTION = "postgres://:password@host:port/dbname"
conn = psycopg.connect("dbname=test user=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM my_data")

# Retrieve query results
records = cur.fetchall()