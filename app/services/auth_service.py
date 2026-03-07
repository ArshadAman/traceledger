import bcrypt
from app.db.pool import pool
from db.audit import INSERT_AUDIT_EVENT
from db.auth import GET_USER_BY_EMAIL
from psycopg2.extras import RealDictCursor


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


def login_user(conn, email: str, password: str) -> bool:
    conn = pool.getconn()
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
