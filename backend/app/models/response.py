from pydantic import BaseModel
from typing import List, Optional

class Error(BaseModel):
    category: str
    location: str
    message: str
    suggestion: str
    justification: str

class AnalysisResponse(BaseModel):
    errors: List[Error]
    summary: str

class ErrorResponse(BaseModel):
    detail: str 