from typing import Optional
from core.metrics import increment_error, increment_login, increment_request, get_metrics
from core.errors import raise_api_error
from fastapi import APIRouter
from schemas.audit_events import AuditEventListResponse
from schemas.auth import LoginRequest, LoginResponse
from schemas.search import AuditSearchResponse
from schemas.users import CreateUserRequest, UserResponse
from services import audit_service
from services.auth_service import login_user, register_user
from starlette.exceptions import HTTPException
from starlette.requests import Request
from core.logger import logger
from core.rate_limiter import RateLimiter
from db.connection import get_db_conn
from db.pool import pool
from cache.redis_client import redis_client
from messaging.rabbitmq import get_rabbit_con
from search.client import es

# Initialize a router
router = APIRouter()
rate_limiter = RateLimiter(limit=100, window=60)


# ------------System----------------
@router.get("/metrics", tags=["system"])
def metrics():
    increment_request()
    return get_metrics()

@router.get("/health")
def health_check():
    status = {
        "api": "ok",
        "database": "unknown",
        "redis": "unknown",
        "rabbitmq": "unknown",
        "elasticsearch": "unknown"
    }

    # DB check
    try:
        conn = get_db_conn()
        pool.putconn(conn)
        status["database"] = "ok"
    except Exception:
        status["database"] = "fail"

    # Redis check
    try:
        redis_client.ping()
        status["redis"] = "ok"
    except Exception:
        status["redis"] = "fail"

    # RabbitMQ check
    try:
        connection = get_rabbit_con()
        connection.close()
        status["rabbitmq"] = "ok"
    except Exception:
        status["rabbitmq"] = "fail"

    # Elasticsearch check
    try:
        if es.ping():
            status["elasticsearch"] = "ok"
        else:
            status["elasticsearch"] = "fail"
    except Exception:
        status["elasticsearch"] = "fail"

    return status

# ---------Auth------------
@router.post("/auth/login", tags=["auth"], response_model=LoginResponse)
def login(payload: LoginRequest):
    increment_request()
    success = login_user(payload.email, payload.password)
    increment_login()
    if not success:
        increment_error()
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "Login Successful"}


# ----------USERS------------
@router.post("/users", tags=["users"], response_model=UserResponse, status_code=201)
def create_user(payload: CreateUserRequest):
    increment_request()
    user_id, status = register_user(payload.email, payload.password)
    if status != 201:
        increment_error()
        raise_api_error(400, "User creation failed")
    return {"id": user_id, "email": payload.email}


@router.get("/users/me", tags=["users"])
def get_my_profile():
    increment_request()
    return {"message": "get my profile endpoint"}


@router.get("/users/{user_id}", tags=["users"])
def get_user(user_id: str):
    increment_request()
    user = get_user(user_id)
    if not user:
        increment_error()
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", tags=["users"])
def update_user(user_id: int):
    return {"message": "Update user endpoint"}


# ------------AUDIT EVENTS--------------
@router.get(
    "/audit-events", tags=["audit-events"], response_model=AuditEventListResponse
)
def list_audit_events(
    actor_id: Optional[int] = None,
    action: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    increment_request()
    return {
        "total": 1,
        "items": [
            {
                "id": 1,
                "actor_id": actor_id or 1,
                "action": action or "USER_LOGIN",
                "status": "success",
                "created_at": "2026-01-01T10:00:00",
            }
        ],
    }


@router.get("/audit-events/search", response_model=AuditSearchResponse)
def search_audit_logs(
    request: Request,
    q: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    increment_request()
    user_key = request.client.host if request.client else "anonymous"
    if rate_limiter.allow_request(user_key):
        increment_error()
        raise HTTPException(status_code=429, detail="Rate Limit Exceeded")
    res = audit_service.es_search(q, start, end, limit, offset)
    if res.get("degraded"):
        # Logging
        logger.warning("Service Degraded")
    return res

@router.get("/audit-events/{event_id}", tags=["audit-events"])
def get_audit_event(event_id: int):
    increment_request()
    return {"event_id": event_id}


@router.get(
    "/users/{user_id}/audit-events",
    tags=["audit-events"],
    response_model=AuditEventListResponse,
)
def get_user_audit_events(
    user_id: int, action: Optional[str] = None, limit: int = 20, offset: int = 0
):
    increment_request()
    return {
        "total": 1,
        "items": [
            {
                "id": 1,
                "actor_id": user_id or 1,
                "action": action or "USER_LOGIN",
                "status": "success",
                "created_at": "2026-01-01T10:00:00",
            }
        ],
    }


# --------------INTERNAL---------------
@router.post("/internal/audit-events", tags=["internal"])
def create_internal_audit_events():
    increment_error()
    return {"message": "Inernal audit events"}
