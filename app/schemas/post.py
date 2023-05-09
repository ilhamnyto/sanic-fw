from dataclasses import dataclass
from datetime import datetime

@dataclass
class PostData:
    id: str
    username: str
    body: str
    created_at: str
    
@dataclass
class Paging:
    cursor: str
    next: bool

@dataclass
class PostResponse:
    status: int
    data: PostData
    paging: Paging
