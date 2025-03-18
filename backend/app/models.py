from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Document(Base):
    __tablename__ = "extracted_details" # This defines a database table named "extracted_details". The class Document represents a row in the "extracted_details" table.

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    # client_name = Column(String) # client name if logged in
    file_name = Column(String) # filename of uploaded file
    extrated_placeholders = Column(Text) # json data of extracted placeholders