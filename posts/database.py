import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
    password = 'bira', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connected Successfully.")
except Exception as error:
    print("Database Failed to connect.")
    print({"Error": error})
    time.sleep(5)