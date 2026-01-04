from fastapi import FastAPI, UploadFile, File
import pdfplumber
from test_spicy import extract_skills

app = FastAPI(title="Resume Skill Intelligence API")


@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "skills_found": skills,
        "total_skills": len(skills)
    }