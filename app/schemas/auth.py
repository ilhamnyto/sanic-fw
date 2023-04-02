from dataclasses import dataclass

@dataclass
class UserLoginResponse:
    access_token: str
    status: int