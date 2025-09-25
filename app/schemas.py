from pydantic import BaseModel
from typing import Union, Dict, List

class QueryRequest(BaseModel):
    query_type: str   # "question" or "offer"
    content: str
    metadata: Union[Dict, None] = None

class OfferItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total_price: float

class OfferResponse(BaseModel):
    project_title: str
    items: List[OfferItem]
    total: float
    notes: str

class QueryResponse(BaseModel):
    query_type: str
    input: str
    output: Union[str, OfferResponse]
