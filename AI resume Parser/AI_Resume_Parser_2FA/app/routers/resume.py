from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Resume
from ..services.resume_parser import extract_text, parse_resume

router = APIRouter(prefix="/api/v1/resume", tags=["Resume"])

@router.post("/parse")
async def parse_uploaded_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(400, "Upload a PDF or DOCX resume")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(413, "File size must be 5 MB or less")
    try:
        raw = extract_text(file.filename, content)
    except Exception as exc:
        raise HTTPException(400, f"Could not parse resume: {exc}")
    data = parse_resume(raw)
    record = Resume(filename=file.filename, extracted_text=raw, extracted_data=data)
    db.add(record)
    await db.commit()
    return {"resume_id": record.id, "extracted_text": raw, "data": data}
