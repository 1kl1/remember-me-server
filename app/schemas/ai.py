from typing import Optional
from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str

class DocumentInput(BaseModel):
    text: str
    metadata: Optional[dict] = {}