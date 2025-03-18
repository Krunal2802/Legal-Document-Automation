from pydantic import BaseModel
from typing import Optional

# Schema for reading (retrieving) document data
class DocumentBase(BaseModel):
    file_name: str  # Filename of the uploaded file
    extrated_placeholders: str  # JSON data of extracted placeholders (stored as text)

# Schema for creating a new document (does not include id)
class DocumentCreate(DocumentBase):
    pass  # Inherits all fields from DocumentBase

# Schema for reading a document with id
class DocumentRead(DocumentBase):
    id: int  # Auto-incremented ID

    class Config:
        from_attributes = True  # Enables ORM mode (to work with SQLAlchemy models)