from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    location: str
    password: str
    salt: str    
    created_at: datetime
    updated_at: datetime
    id : Optional[int] = None
