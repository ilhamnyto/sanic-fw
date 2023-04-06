from dataclasses import dataclass
from datetime import datetime

@dataclass
class PostData:
    id: str
    user_id: int
    body: int
    created_at: datetime

@dataclass
class PostResponse:
    status: int
    data: PostData