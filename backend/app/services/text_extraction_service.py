import io
import pdfplumber
import docx
from typing import Optional
from fastapi import UploadFile

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts text from a PDF file.
    """
    text = ""
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n" if page.extract_text() else ""
    return text.strip()

def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extracts text from a DOCX file.
    """
    text = ""
    doc = docx.Document(io.BytesIO(file_content))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()

def extract_text_from_txt(file_content: bytes) -> str:
    """
    Extracts text from a TXT file.
    """
    return file_content.decode("utf-8").strip()

def extract_text_from_pdf_or_doc(file: UploadFile, content: bytes) -> Optional[str]:
    """
    Determines file type and extracts text from PDF, DOCX, or TXT files.
    """
    file_extension = file.filename.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(content)
    elif file_extension == "docx":
        return extract_text_from_docx(content)
    elif file_extension == "txt":
        return extract_text_from_txt(content)
    else:
        return ""
