from typing import Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    status: Optional[int]
    message: str
