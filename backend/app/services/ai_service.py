import json
from langchain.chat_models import ChatOpenAI
from app.config import OPENAI_API_KEY
from app.services.text_extraction_service import extract_text_from_pdf_or_doc
from app.services.ocr_service import extract_text_from_image
from fastapi import UploadFile

# Initialize OpenAI Chat Model
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

def process_document(file: UploadFile, content: bytes) -> dict:
    """
    Extracts text from the uploaded document (PDF, DOCX, TXT, or image).
    Combines all extracted text before sending it to AI for processing.
    """
    # Extract text from digital documents (PDF, DOCX, TXT)
    extracted_text = extract_text_from_pdf_or_doc(file, content)

    # Extract text from images using OCR
    ocr_text = extract_text_from_image(content)

    # Combine both extracted texts
    full_text = f"{extracted_text}\n{ocr_text}".strip()

    if not full_text:
        return {"error": "No extractable text found in the document."}

    # Define prompt with JSON structure
    prompt = f"""
    Extract key legal entities and missing clauses from the following document. 
    Return the result strictly in JSON format.

    The JSON structure should be:
    {{
        "placeholders": {{
            "SimpleKey1": "Value1",
            "SimpleKey2": "Value2",
            "NestedKey": {{
                "SubKey1": "SubValue1",
                "SubKey2": "SubValue2"
            }},
            "MissingClauses": {{
                "Clause1": "Clause details",
                "Clause2": "Clause details"
            }}
        }}
    }}

    Document:
    {full_text}

    Ensure the response is **valid JSON** with no additional text.
    """

    # Get AI response
    response = llm.invoke(prompt)

    try:
        return json.loads(response)  # Convert response to JSON
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from model"}
