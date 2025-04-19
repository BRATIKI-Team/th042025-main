from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel


class MessageModel(BaseModel):
    id: Optional[int] = None
    source_id: int
    content: str
    external_id: str
    created_at: datetime
    published_at: Optional[datetime] = None
    metadata: Dict[str, Any] 