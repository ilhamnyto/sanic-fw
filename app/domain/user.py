from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    username: str
    email: str
    password: str
    salt: str    
    id : Optional[int] = None
