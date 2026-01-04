import spacy
from skills import skills

nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str):
    text = text.lower()
    extracted_skills = []

    for skill in skills:
        if skill in text:
            extracted_skills.append(skill)

    return list(set(extracted_skills))  # return unique skills

