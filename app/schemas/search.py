from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AuditSearchResult(BaseModel):
    actor_id: Optional[str]
    action: str
    status: str
    message: Optional[str]
    timestamp: datetime
    
class AuditSearchResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[AuditSearchResult]
    