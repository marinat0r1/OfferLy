from pydantic import BaseModel, Field
from typing import Union, Dict, List, Optional, Type

# ----- Header / nested models -----
class Contact(BaseModel):
    phone: Optional[str] = "TBD"
    email: Optional[str] = "TBD"

class Sender(BaseModel):
    company_name: str = "TBD"
    address: str = "TBD"
    contact: Contact = Contact()
    icon: Optional[str] = "TBD"

class Recipient(BaseModel):
    company_name: str = "TBD"
    contact_person: Optional[str] = "TBD"
    address: Optional[str] = "TBD"

class Metadata(BaseModel):
    document_type: str = "Offer"
    date: str = "TBD"
    reference_number: Optional[str] = "TBD"
    subject: Optional[str] = "TBD"

class Header(BaseModel):
    sender: Sender = Sender()
    recipient: Recipient = Recipient()
    metadata: Metadata = Metadata()

# ----- Original OfferItem unchanged -----
class OfferItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total_price: float

# ----- OfferResponse updated with header and placeholders -----
class OfferResponse(BaseModel):
    header: Header = Header()
    project_title: str = "TBD"
    items: List[OfferItem] = []
    total: float = 0.0
    notes: str = "TBD"

# ----- Query models unchanged -----
class QueryRequest(BaseModel):
    query_type: str   # "question" or "offer"
    content: str
    metadata: Union[Dict, None] = None

class QueryResponse(BaseModel):
    query_type: str
    input: str
    output: Union[str, OfferResponse]

