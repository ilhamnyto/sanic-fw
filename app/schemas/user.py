from dataclasses import dataclass
from typing import List

@dataclass
class User:
    username: str
    email: str

@dataclass
class Paging:
    next: str
    previous: str

@dataclass
class UserResponse:
    status: int
    data: List[User]
    paging: Paging
