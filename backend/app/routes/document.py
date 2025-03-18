from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_service import process_document
from app.services.ocr_service import extract_text_from_image
from app.services.text_extraction_service import extract_text_from_pdf_or_doc
from app.models import Document
from app.schemas import DocumentCreate, DocumentRead
from typing import List

router = APIRouter()

@router.post("/upload/", response_model=DocumentRead)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a document, extract text from both digital documents (PDF, DOCX, TXT) and images (OCR),
    process it with AI, and store it in the database.
    """
    content = await file.read()
    
    # Extract text from document (PDF, DOCX, TXT)
    digital_text = extract_text_from_pdf_or_doc(file, content)
    
    # Extract text from images using OCR
    image_text = extract_text_from_image(content)

    # Combine both extracted texts
    full_text = f"{digital_text}\n{image_text}".strip()

    if not full_text:
        raise HTTPException(status_code=400, detail="No text could be extracted from the document.")

    processed_text = process_document(full_text)  # Process with AI

    doc = Document(file_name=file.filename, extrated_placeholders=processed_text)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc

@router.get("/documents/", response_model=List[DocumentRead])
def get_documents(db: Session = Depends(get_db)):
    """
    Retrieve a list of all uploaded documents.
    """
    return db.query(Document).all()

@router.get("/documents/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific document by its ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
