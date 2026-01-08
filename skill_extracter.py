import spacy
from skills import skills
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

patterns = [nlp.make_doc(skill)for skill in skills]
matcher.add("skills", patterns)

def extract_skills(text: str):
    doc = nlp(text)
    matches = matcher(doc)

    found_skills = set()

    for _, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text.lower())

    return list(found_skills)
    

