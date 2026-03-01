from datetime import datetime
from pydantic import BaseModel
from typing import List

class AuditEventResponse(BaseModel):
    id: int
    actor_id: int
    action: str
    status: str
    created_at: datetime
    
class AuditEventListResponse(BaseModel):
    total: int
    items: List[AuditEventResponse]