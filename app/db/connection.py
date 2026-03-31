from app.db import pool

def get_db_conn():
    return pool.pool.getconn()
    
# print(get_db_conn())