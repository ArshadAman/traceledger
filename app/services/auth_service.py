import json
from messaging.publisher import publish_event
from cache.redis_client import redis_client
from db.pool import pool
from security.password_verfication import verify_password
from db.audit import INSERT_AUDIT_EVENT
from db.users import CREATE_USER, GET_USER_BY_EMAIL, GET_USER_BY_ID
from psycopg2.extras import RealDictCursor
from security.hashing import hash_password
from db.connection import get_db_conn

def login_user(email: str, password: str) -> bool:
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(GET_USER_BY_EMAIL, (email,))
            user = cur.fetchone()
    
            if not user:
                publish_event(
                    "USER_LOGIN_FAILED",
                    {
                        "user_id": email,
                        "reason": "user not found",
                        "status": "failed"
                    }
                )
                return False
    
            # Password
            if not verify_password(password, user["password_hash"]):
                publish_event("USER_LOGIN_FAILED", {"user_id": str(user["id"]), "reason": "invalid password", "status": "failed"})
                return False
            # Success
            publish_event(
                "USER_LOGIN_SUCCESS",
                {
                    "user_id": str(user["id"]),
                    "method": "password",
                    "status": "success"
                }
            )
            return True
    finally:
        pool.putconn(conn)

def register_user(email: str, password: str):
    conn = get_db_conn()
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
            if user:
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
                return user["id"], True
            else:
                return None, False
    finally:
        pool.putconn(conn)

# GET user service
def get_user(user_id):
    """Fetch a user using cache-aside strategy"""
    
    # create a cache key
    cache_key = f"user:{user_id}"
    
    # Check the cache
    cached_user = redis_client.get(cache_key)
    if cached_user:
        # if data exits in Redis, convert JSON String to python dict
        return json.loads(str(cached_user))
    
    # if there is cache miss
    conn = get_db_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curr:
            curr.execute(GET_USER_BY_ID, (user_id,))
            user = curr.fetchone()
    finally:
        pool.putconn(conn)
    # store it in the cache
    redis_client.set(
        cache_key,
        json.dumps(user),
        ex=60
    )
    return user