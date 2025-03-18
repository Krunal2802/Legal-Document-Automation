from fastapi import FastAPI
from app.routes import document

app = FastAPI(title="Legal Document Automation API")

app.include_router(document.router, prefix="/docs", tags=["Documents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)