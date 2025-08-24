from nlp.intent import classify_intent
from jinja2 import Template
import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

def render_template(jinja_str: str, ctx: dict) -> dict:
    t = Template(jinja_str)
    full = t.render(**ctx)
    lines = full.splitlines()
    subject = lines[0].replace("Subject:", "").strip() if lines and lines[0].startswith("Subject:") else ""
    body = ("\n".join(lines[1:]) if subject else full).strip()
    return {"subject": subject, "body_text": body, "body_html": body.replace("\n", "<br>")}

def generate_reply(intent, subject, body, sender_name):
    prompt = f"""
    You are a helpful, professional AI email assistant. You help respond to inbound emails, 
    follow-up threads, and ongoing conversations in a natural, human-like way.
    
    Write a reply to the following email:

    Intent: {intent}
    Subject: {subject}
    Body: {body}

    Rules:
    1. Always starts with: "Hi {sender_name},"
    2. Always has the first sentence: "Thank you for your email."
    3. After that, generate a personalized and relevant reply based on the intent and body.
    4. Keep tone polite, professional, and natural.
    5. Write at most 4 sentences
    6. End with: "Best regards, John"
    """
    respond = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return respond.choices[0].message["content"].strip()
 
if __name__ == "__main__":
    emails = load_emails()

    for email in emails:
        sender_name = extract_name(email["sender"])
        intent = classify_email(email["subject"], email["body"])
        reply = generate_reply(intent, email["subject"], email["body"], sender_name)

        print(f"--- Email from {email['sender']} ---")
        print(f"Intent: {intent}")
        print(f"Draft Reply:\n{reply}\n")
