from dataclasses import dataclass
from typing import List

@dataclass
class User:
    username: str
    email: str
    created_at: str

@dataclass
class Paging:
    cursor: str
    next: bool

@dataclass
class UserResponse:
    status: int
    data: List[User]
    paging: Paging
