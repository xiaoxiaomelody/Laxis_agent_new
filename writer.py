from jinja2 import Template

MEETING_J2 = """Subject: {{ subject }}
Hi {{ candidate_name or 'there' }},

Thanks for your reply! {{ customer_name }} can meet {{ meeting_time }}. 
Let me know if that works for you.

Best regards,
{{ customer_name }}
{{ customer_title }} | {{ customer_company }}
"""

def render_template(jinja_str: str, ctx: dict) -> dict:
    t = Template(jinja_str)
    full = t.render(**ctx)
    # 简单切分出 Subject 行
    lines = full.splitlines()
    subject = lines[0].replace("Subject:", "").strip()
    body = "\n".join(lines[1:]).strip()
    return {"subject": subject, "body_text": body, "body_html": body.replace("\n", "<br>")}
