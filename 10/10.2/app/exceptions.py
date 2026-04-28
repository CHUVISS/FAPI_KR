from pydantic import BaseModel
from typing import List, Any

class ValidationErrorResponse(BaseModel):
    status_code: int = 422
    message: str = "Validation Failed"
    details: List[dict[str, Any]]