from app.services.resume_parser import parse_resume

def test_parse_resume_extracts_email_and_skills():
    result = parse_resume("Jane Doe\njane@example.com\nPython SQL FastAPI")
    assert result["name"] == "Jane Doe"
    assert result["email"] == "jane@example.com"
    assert "Python" in result["skills"]
