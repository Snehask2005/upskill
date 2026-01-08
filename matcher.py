import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

CORE_KEYWORDS = ["must", "required", "need", "necessary", "essential", "mandatory",'strong', 'experience', 'proficient', 'expert','extensive', 'in-depth', 'hands-on']
SECONDARY_KEYWORDS = ["preferred", "nice-to-have", "bonus", "advantageous", "good to have", "familiarity", "knowledge of", "exposure to", "plus"]


def classify_job_skills(job_description: str, job_skills: list):
    
    doc = nlp(job_description.lower())

    core_skills = set()
    secondary_skills = set()
    frequency = defaultdict(int)

    for sent in doc.sents:
        sent_text = sent.text
        for skill in job_skills:
            if skill in sent_text:
                frequency[skill] +=1

                if any(k in sent_text for k in CORE_KEYWORDS):
                    core_skills.add(skill)
                
                elif any(k in sent_text for k in SECONDARY_KEYWORDS):
                    secondary_skills.add(skill)
    
    for skill, count in frequency.items():
        if count >= 2 and skill not in secondary_skills:
            core_skills.add(skill)
        elif skill not in core_skills:
            secondary_skills.add(skill)
    return list(core_skills), list(secondary_skills)


def match_skills(resume_skills: list, job_skills: list, job_description: str):

    core_skills, secondary_skills = classify_job_skills(job_description, job_skills)

    matched = []
    missing = []
    score = 0

    CORE_WEIGHT = 10
    SECONDARY_WEIGHT = 5

    max_score = (len(core_skills) * CORE_WEIGHT) + (len(secondary_skills) * SECONDARY_WEIGHT)

    for skill in core_skills:
        if skill in resume_skills:
            matched.append(skill)
            score += CORE_WEIGHT
        else:
            missing.append(skill)
    
    for skill in secondary_skills:
        if skill in resume_skills:
            matched.append(skill)
            score += SECONDARY_WEIGHT
        else:
            missing.append(skill)
    
    percentage = round((score / max_score) * 100, 2) if max_score > 0 else 0

    if percentage >= 70:
        explanation = "Strong Match "
    elif percentage >= 40:
        explanation = "Partial match. Some important skill gaps exist."
    else:
        explanation = "Weak match. Significant skill gaps exist."

    if missing:
        explanation += f" Missing skills: {', '.join(missing)}."

    return {
        "Core Skills": core_skills,
        "Secondary Skills": secondary_skills,
        "Matched Skills": matched,
        "Missing Skills": missing,
        "Score": percentage,
        "Explanation": explanation
    }
    
