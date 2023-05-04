from dataclasses import dataclass
from typing import List

@dataclass
class User:
    username: str
    email: str
    created_at: str

@dataclass
class Paging:
    current: str
    next: str

@dataclass
class UserResponse:
    status: int
    data: List[User]
    paging: Paging
