from typing import Optional

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

from app.core.rate_limiter import RateLimiter

# Initialize a router
router = APIRouter()
rate_limiter = RateLimiter(limit=100, window=60)


# ------------System----------------
@router.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


# ---------Auth------------
@router.post("/auth/login", tags=["auth"], response_model=LoginResponse)
def login(payload: LoginRequest):
    success = login_user(payload.email, payload.password)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "Login Successful"}


# ----------USERS------------
@router.post("/users", tags=["users"], response_model=UserResponse, status_code=201)
def create_user(payload: CreateUserRequest):
    user_id, status = register_user(payload.email, payload.password)
    if status != 201:
        raise_api_error(400, "User creation failed")
    return {"id": user_id, "email": payload.email}


@router.get("/users/me", tags=["users"])
def get_my_profile():
    return {"message": "get my profile endpoint"}


@router.get("/users/{user_id}", tags=["users"])
def get_user(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", tags=["users"])
def update_user(user_id: int):
    # redis_client.delete(f"user:{user_id}") need to done in the service layer
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
    user_key = request.client.host if request.client else "anonymous"
    if rate_limiter.allow_request(user_key):
        raise HTTPException(status_code=429, detail="Rate Limit Exceeded")
    res = audit_service.es_search(q, start, end, limit, offset)
    return res


@router.get("/audit-events/{event_id}", tags=["audit-events"])
def get_audit_event(event_id: int):
    return {"event_id": event_id}


@router.get(
    "/users/{user_id}/audit-events",
    tags=["audit-events"],
    response_model=AuditEventListResponse,
)
def get_user_audit_events(
    user_id: int, action: Optional[str] = None, limit: int = 20, offset: int = 0
):
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
    return {"message": "Inernal audit events"}
