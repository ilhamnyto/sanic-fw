from dataclasses import dataclass

@dataclass
class ErrorResponse:
    status: int
    err_code: str
    message: str

@dataclass
class SuccessResponse:
    status: int
    message: str
