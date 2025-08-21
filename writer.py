# agents/writer.py
from jinja2 import Template

def render_template(jinja_str: str, ctx: dict) -> dict:
    t = Template(jinja_str)
    full = t.render(**ctx)
    lines = full.splitlines()
    subject = lines[0].replace("Subject:", "").strip() if lines and lines[0].startswith("Subject:") else ""
    body = ("\n".join(lines[1:]) if subject else full).strip()
    return {"subject": subject, "body_text": body, "body_html": body.replace("\n", "<br>")}
