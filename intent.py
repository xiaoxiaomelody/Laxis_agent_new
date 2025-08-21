import re

RULES = [
    ("meeting_request", r"\b(available|schedule|meet|call|zoom|calendar)\b"),
    ("follow_up",       r"\b(follow\s*up|checking in|any update)\b"),
    ("reschedule",      r"\b(reschedule|another time|push back|postpone)\b"),
    ("rejection",       r"\b(no longer|not interested|decline)\b"),
]

def rule_intent(text):
    low = text.lower()
    for label, pat in RULES:
        if re.search(pat, low):
            return label
    return "general"

# 可选：LLM 兜底 → 返回 {intent: "...", confidence: 0.8}
def llm_intent_fallback(text) -> dict:
    # 调 OpenAI / 其他 LLM，要求以 JSON 返回
    return {"intent": "general", "confidence": 0.5}

def classify_intent(text) -> str:
    label = rule_intent(text)
    if label == "general":
        res = llm_intent_fallback(text)
        return res["intent"]
    return label
