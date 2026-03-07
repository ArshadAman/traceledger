from typing import Optional

from db.connecction import get_db_conn
from fastapi import APIRouter
from schemas.audit_events import AuditEventListResponse
from schemas.auth import LoginRequest, LoginResponse
from schemas.users import CreateUserRequest, UserResponse
from services.auth_service import login_user
from starlette.exceptions import HTTPException

# Initialize a router
router = APIRouter()


# ------------System----------------
@router.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


# ---------Auth------------
@router.post("/auth/login", tags=["auth"], response_model=LoginResponse)
def login(payload: LoginRequest):
    conn = get_db_conn()
    success = login_user(conn, payload.email, payload.password)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "Login Successful"}


# ----------USERS------------
@router.post("/users", tags=["users"], response_model=UserResponse, status_code=201)
def create_user(payload: CreateUserRequest):
    return {"id": 1, "email": payload.email}


@router.get("/users/me", tags=["users"])
def get_my_profile():
    return {"message": "get my profile endpoint"}


@router.get("/users/{user_id}", tags=["users"])
def get_user(user_id: int):
    return {"message": "Get user endpoint"}


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
