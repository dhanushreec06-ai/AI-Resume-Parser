import re
from pathlib import Path
from docx import Document
import pdfplumber

SKILL_WORDS = ["Python", "Java", "C", "C++", "SQL", "FastAPI", "Django",
               "Machine Learning", "Deep Learning", "HTML", "CSS", "JavaScript",
               "PostgreSQL", "AWS", "Git", "Docker", "Pandas", "NumPy"]

def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        import io
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if suffix == ".docx":
        import io
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Only PDF and DOCX files are supported")

def parse_resume(text: str) -> dict:
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone_match = re.search(r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)", text)
    skills = [s for s in SKILL_WORDS if re.search(r"\b" + re.escape(s) + r"\b", text, re.I)]
    name = lines[0][:150] if lines else ""
    return {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0).strip() if phone_match else None,
        "skills": skills,
        "experience": None,
        "qualification": None
    }
