from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    username: str
    email: str
    password: str
    salt: str    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id : Optional[int] = None
