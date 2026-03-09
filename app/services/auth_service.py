from app.db.pool import pool
from app.security.password_verfication import verify_password
from db.audit import INSERT_AUDIT_EVENT
from db.users import CREATE_USER, GET_USER_BY_EMAIL
from psycopg2.extras import RealDictCursor
from security.hashing import hash_password
from db.connection import get_db_conn

def login_user(conn, email: str, password: str) -> bool:
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(GET_USER_BY_EMAIL, (email,))
            user = cur.fetchone()
    
            if not user:
                cur.execute(
                    INSERT_AUDIT_EVENT,
                    (
                        None,
                        "system",
                        "USER_LOGIN",
                        "user",
                        "failure",
                        {"reason": "user not found"},
                    ),
                )
                conn.commit()
                return False
    
            # Password
            if not verify_password(password, user["password_hash"]):
                cur.execute(
                    INSERT_AUDIT_EVENT,
                    (
                        user["id"],
                        "user",
                        "USER_LOGIN",
                        "failure",
                        {"reason": "Invalid credentials"},
                    ),
                )
                conn.commit()
                return False
            # Success
            cur.execute(
                INSERT_AUDIT_EVENT,
                (
                    user["id"],
                    "user",
                    "USER_LOGIN",
                    "success",
                    {"method": "password"}
                )
            )
            conn.commit()
            return True
    finally:
        pool.putconn(conn)

def register_user(conn, email: str, password: str):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            password_hash = hash_password(password)
            cur.execute(GET_USER_BY_EMAIL, (email,))
            existing_user = cur.fetchone()
            if existing_user:
                cur.execute(
                    INSERT_AUDIT_EVENT,
                    (
                        None,
                        "user",
                        "USER_REGISTER",
                        "user",
                        "failure",
                        {"reason": "User already exits"}
                    )
                )
                return None, False
            cur.execute(
               CREATE_USER, 
              (email, password_hash, "user") 
            )
            user = cur.fetchone()
            cur.execute(
                INSERT_AUDIT_EVENT,
                (
                    user["id"],
                    "user",
                    "USER_REGISTER",
                    "user",
                    "success",
                    {"method": "password"}
                )
            )
            conn.commit()
            return user["id"]
    finally:
        pool.putconn(conn)