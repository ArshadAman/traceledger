from psycopg2.pool import SimpleConnectionPool
from app.core.config import settings

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=settings.db_name,
    user=settings.db_user,          
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port
)