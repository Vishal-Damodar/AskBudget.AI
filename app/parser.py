import os
from fastapi import APIRouter, UploadFile, File, Form
from app.parser import parse_statement
import tempfile

router = APIRouter()

@router.post("/upload/")
async def upload_statement(
    file: UploadFile = File(...),
    source: str = Form(...)
):
    """
    Upload a bank/payment CSV and return normalized transactions.
    Supported sources: phonepe, google_pay
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        data = parse_statement(tmp_path, source)
        os.remove(tmp_path)
        return {"transactions": data}

    except Exception as e:
        return {"error": str(e)}
