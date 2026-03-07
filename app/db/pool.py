from psycopg2.pool import SimpleConnectionPool

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname="traceledger",
    password="",
    host="localhost",
    port = 5432
)