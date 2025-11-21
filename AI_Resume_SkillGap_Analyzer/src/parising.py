# src/parsing.py
import re
from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")

# small canonical skill list (expandable)
CANONICAL_SKILLS = [
    "python","sql","machine learning","deep learning","tensorflow",
    "pytorch","nlp","data visualization","aws","docker","kubernetes",
    "spark","pandas","scikit-learn","statistics","git"
]

def text_from_file(path):
    if path.endswith(".txt"):
        return open(path, "r", encoding="utf-8").read()
    # add pdf/docx extraction as needed
    raise NotImplementedError("Only txt supported in this minimal extractor")

def extract_skills(text):
    text_low = text.lower()
    found = set()
    # exact substring matching first (simple & effective)
    for skill in CANONICAL_SKILLS:
        if skill in text_low:
            found.add(skill)
    # entity extraction (optional)
    doc = nlp(text)
    # example: pick up ORG/PRODUCT nouns as keywords (lightweight)
    tokens = [t.lemma_.lower() for t in doc if not t.is_stop and t.is_alpha]
    # frequency hint
    common = Counter(tokens).most_common(40)
    # return sorted list
    return sorted(found)
