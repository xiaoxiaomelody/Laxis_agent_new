import spacy
_nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str):
    ents = {"PERSON": [], "ORG": [], "DATE": []}
    for e in _nlp(text or "").ents:
        if e.label_ in ents:
            ents[e.label_].append(e.text)
    return ents
