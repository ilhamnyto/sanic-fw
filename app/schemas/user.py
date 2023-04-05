from dataclasses import dataclass
from typing import List

@dataclass
class User:
    username: str
    email: str

@dataclass
class UserResponse:
    status: int
    data: List[User]
