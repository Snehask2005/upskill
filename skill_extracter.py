import spacy
from skills import skills
from spacy.matcher import PhraseMatcher
from skills import skills
from aliases import ALIASES

nlp = spacy.load("en_core_web_sm")


matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in skills]
matcher.add("skills", patterns)

def extract_skills(text: str):
    doc = nlp(text.lower())

    matches = matcher(doc)
    found_skills = set()

    for _, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text.lower())

    lemmas = {token.lemma_ for token in doc}

    for skill in skills:
        if skill in lemmas:
            found_skills.add(skill)

    normalized_skills = set()

    for skill in found_skills:
        mapped = False
        for canonical, aliases in ALIASES.items():
            if skill == canonical or skill in aliases:
                normalized_skills.add(canonical)
                mapped = True
                break
        if not mapped:
            normalized_skills.add(skill)

    return list(normalized_skills)
    

