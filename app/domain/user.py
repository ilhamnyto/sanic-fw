from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    username: str
    email: str
    password: str
    salt: str    
    first_name: str
    last_name: str
    phone_number: str
    location: str
    created_at: datetime
    updated_at: datetime
    id : Optional[int] = None
