from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
from skill_extracter import extract_skills
from matcher import match_skills
from fastapi import Body



app = FastAPI(title="Resume Skill Intelligence API")




@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/analuze-resume/")

async def upload_resume(file: UploadFile = File(...), job_description: str = Form(...)):

    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}
    

    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    result = match_skills(skills, job_skills, job_description)

    return {
        "filename": file.filename,
        "skills_found": skills,
        "total_skills": len(skills),
        "job_required_skills": job_skills,
        "Analysis": result
    }

