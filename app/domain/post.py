from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Post:
    user_id: int
    body: str
    created_at: datetime
    id: Optional[int] = None

@dataclass
class PostData:
    posts_id: int
    username: str
    body: str
    created_at: str