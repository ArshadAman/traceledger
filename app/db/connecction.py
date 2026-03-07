import psycopg2


def get_db_conn():
    return psycopg2.connect(
        dbname="traceledger",
        user="arshadaman",
        password="",
        host="localhost",
        port=5432
    )
    
# print(get_db_conn())