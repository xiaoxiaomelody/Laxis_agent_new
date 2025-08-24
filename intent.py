import re
import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

RULES = [
    ("meeting_request", r"\b(available|schedule|meet|call|zoom|calendar)\b"),
    ("follow_up",       r"\b(follow\s*up|checking in|any update)\b"),
    ("reschedule",      r"\b(reschedule|another time|push back|postpone)\b"),
    ("rejection",       r"\b(no longer|not interested|decline)\b"),
    ("inquiry",         r"\b(question|ask|wonder|clarify|information|details|concern)\b"),
]

def rule_intent(text: str) -> str:
    low = text.lower()
    for label, pat in RULES:
        if re.search(pat, low):
            return label
    return "general"

def llm_intent_fallback(subject: str, body: str) -> str:
    prompt = f"""
    Classify this email into one of these categories:
    - Inquiry
    - Meeting Request
    - Follow-Up
    - Objection
    - Other

    Subject: {subject}
    Body: {body}

    Respond with only the category name.
    """
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message["content"].strip().lower().replace(" ", "_")
    except Exception as e:
        print("LLM fallback failed:", e)
        return "general"

def classify_intent(subject: str, body: str) -> str:
    text = subject + " " + body
    label = rule_intent(text)
    
    if label == "general":
        return llm_intent_fallback(subject, body)
    return label


